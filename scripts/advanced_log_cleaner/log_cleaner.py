import subprocess
from os.path import isfile,join
from os import listdir,environ
from stat import S_ISREG, ST_CTIME, ST_MODE
import time
import os
from psutil import disk_partitions
import glob
import sys
import argparse
import fnmatch
import re
import signal

#TODO
#exceptions
#replace sys.stdout. with print
#

def terminateProcess(signalNumber, frame):
    """Receives a fatal signal and exits the program. Exit code is 128+SIGNAL"""
    sys.stderr.write('Received: SIG'+str(signalNumber)+' terminating the process\n')
    sys.exit(128+signalNumber)
    return



def receiveSignal(signalNumber, frame):
    """Receives a non-fatal signal and logs it to stderr."""
    sys.stderr.write('Received: SIG'+str(signalNumber)+' ,ingoring it.\n' )
    return



def partly_truncate_file(file,file_end_size,file_current_size):
    """Uses fallocate to truncate file from beginning.\n
       Starts from byte 0 and adds zeroes(from fallocate) until byte(file_current_size - file_end_size)."""

    try:

        command="/usr/bin/fallocate -p -o 0 -l "+str(int(file_current_size) - int(file_end_size))+" "+file
        print(command)
        subprocess.check_output([command], shell=True, stderr=subprocess.PIPE)
            
    except subprocess.CalledProcessError:
            sys.stderr.write("Could not truncate file using fallocate "+file+"\n")
            sys.exit(1)            



def too_many_files_in_directory_ls(directory,max_files,file_counter,pattern):
    """Called when a directory is over the maximum allowed files. By default it removes the oldest files\n
       Deletes as many files as necessary to get to the given limt(max_files option when running the script)"""
    
    sys.stdout.write("Directory "+directory+" has too many files.("+str(int(file_counter)-int(max_files))+ " over the limit)\nStarting cleanup procedure\n")    
    date_file_list = []
    
    files = [f for f in os.listdir(directory) if os.path.isfile(directory+f)]
    for file in fnmatch.filter(files, pattern):
        file = directory+file
        print("file is " +file)
        stats = os.stat(file)
        lastmod_date = time.localtime(stats[8])
        date_file_tuple = lastmod_date, file
        date_file_list.append(date_file_tuple)
        
    date_file_list.sort()
    #date_file_list.reverse()                                   # If we want the newest files first
    print("%-40s %s" % ("filename:", "last modified:"))
    for file in date_file_list:
        folder, file_name = os.path.split(file[1])# just the filename
        file_date = time.strftime("%m/%d/%y %H:%M:%S", file[0]) # convert date  to MM/DD/YYYY HH:MM:SS 
        print("%-40s %s" % (file_name, file_date))
        #print("Removing "+file_name)
        file_counter-=1;
        if(max_files >= file_counter):
            #print("Removed all necessary files")
            return file_counter
            
    sys.stderr.write("Unable to remove enough files to satisfy max_files argument in directory"+directory+"\n")
    sys.exit(1)


    
def too_many_files_in_directory_rm(directory,max_files,file_counter,pattern):
    """Called when a directory is over the maximum allowed files. By default it removes the oldest files.\n
       Retruns amount of files left in directory. Deletes as many files as necessary until max_files(option) is reached\n"""

    sys.stdout.write("Directory "+directory+" has too many files.("+str(int(file_counter)-int(max_files))+ " over the limit)\nStarting cleanup procedure\n")    
    date_file_list = []
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(directory+f)]
        for file in fnmatch.filter(files, pattern):
                file = directory+file
                stats = os.stat(file)
                lastmod_date = time.localtime(stats[8])
                date_file_tuple = lastmod_date, file
                date_file_list.append(date_file_tuple)      
        date_file_list.sort()
        
        for file in date_file_list:
            folder, file_name = os.path.split(file[1])              
            os.remove(folder+"/"+file_name)
            print("Removed "+folder+"/"+file_name)
            file_counter-=1;
            if(max_files>=file_counter):
                return(file_counter)
                
        sys.stderr.write("Unable to remove enough files to satisfy max_files argument in directory"+directory+"\n")
        sys.exit(1)
    except OSError:
            sys.stderr.write("Error attempting to delete file: "+folder+"/"+file_name+"\n")
            sys.exit(1)


def check_directory_files_ls(directory,max_files_per_dir,max_age,max_size,pattern,max_files_root_dir):
    """Lists directory files recursively and checks if files match given pattern.\n
       If they do, get their size and ctime, and compare them with given limits.\n
       Will also count files in each subdirectory and the root directory."""
    #This function is mainly for debugging
    
    root_file_counter = 0
    current_time_in_seconds=time.time()
    for root, directories, filenames in os.walk(directory):
            file_counter = 0
            for file in fnmatch.filter(filenames, pattern):
                print("")
                print(file)

                path=root+"/"+file
                file_age_in_seconds= current_time_in_seconds - os.path.getmtime(path)
                file_size = str(os.path.getsize(path))
                file_counter+=1
                
                print(file+" SIZE = "+file_size+" AGE in seconds = "+str(file_age_in_seconds))
        
                if((int(file_size)>int(max_size) or int(file_age_in_seconds)>int(max_age))): 
                    print("==========="+file+" satisfies given pattern")
                    print("File: "+file+" is too big or old enough to be operated on")
                    
            print("Directory "+root+" has "+str(file_counter)+" files")
            
            if file_counter > max_files_per_dir:
                files_left=too_many_files_in_directory_ls(root,max_files_per_dir,file_counter,pattern)
                root_file_counter+=files_left

            else:
                root_file_counter+=file_counter


                
def check_directory_files_rm(directory,max_files_per_dir,max_age,max_size,pattern,max_files_root_dir, run_number=''):    
    """Check directory files recursively if they match the given pattern.\n
       If they do, get their size and ctime, and compare them with given limits. Remove them if necessary.\n
       Will also count files in each subdirectory and the root directory.\n
       If the root directory passes the limit of max_files_root_dir, function will be recalled ONCE with all arguments lowered by 50%\n
       To disable the recalling of the function call it with at extra argument in the end equal to 1"""
    
    try:
        root_file_counter = 0
        current_time_in_seconds=time.time()
        for root, directories, filenames in os.walk(directory):
            file_counter = 0
            for file in fnmatch.filter(filenames, pattern):
                    path=root+"/"+file

                    file_age_in_seconds= current_time_in_seconds - os.path.getmtime(path)
                    file_size = str(os.path.getsize(path))
                    file_counter+=1        
                    if(int(file_size)>int(max_size) or int(file_age_in_seconds)>int(max_age)): 
                            os.remove(path)
                            sys.stdout.write("Removed "+path+"\n")
                            file_counter-=1
            print("file counter is "+str(file_counter))
            
            if file_counter > max_files_per_dir:
                    root_file_counter+=too_many_files_in_directory_rm(root,max_files_per_dir,file_counter,pattern)
                    
            else:
                    root_file_counter+=file_counter

        if run_number!='':
            sys.stdout.write("Finished second run on given root directory. Current counted files:"+str(root_file_counter)+"\n")
            sys.exit(2)            
        
        if root_file_counter > max_files_root_dir:
            sys.stdout.write("Starting second run on root directory with 2x lower requirements. Current counted files in root:"+str(root_file_counter)+"\n")            
            check_directory_files_rm(directory,max_files_per_dir/2,max_age/2,max_size/2,pattern,max_files_root_dir,2)
                
    except OSError:
            sys.stderr.write("Error attempting to delete file: "+file+"\n")
            sys.exit(1)


                
def check_directory_files_trunc(directory,max_files_per_dir,max_age,max_size,pattern,max_files_root_dir,run_number=''):
        """Check directory files recursively if they match the given pattern.\n
       If they do, get their size and ctime, and compare them with given limits.\n
       Truncate the entire file if necessary.\n
       Will also count files in each subdirectory and the root directory.\n
       If a subdirectory passes the limit of maximum_files_per_dir, rm function will be called for the subdirectory.\n
       If the root directory passes the limit of max_files_root_dir, function will be recalled ONCE with all.\n
       arguments lowered by 50%. To disable the recalling of the function call it with at extra argument in the end equal to 1"""
             
        current_time_in_seconds=time.time()
        root_file_counter=0
        for root, directories, filenames in os.walk(directory):
                file_counter = 0
                for file in fnmatch.filter(filenames, pattern):
                    path=root+"/"+file
                    file_age_in_seconds= current_time_in_seconds - os.path.getmtime(path)
                    file_size = str(os.path.getsize(path))
                    file_counter+=1
                    
                    if(int(file_size)>int(max_size) or int(file_age_in_seconds)>int(max_age)):
                            fo = open(path, "w")
                            fo.close()
                            #sys.stdout.write("Emptied "+path+"\n")                            
                            file_counter-=1
                                        
                if file_counter > max_files_per_dir:
                        files_left=too_many_files_in_directory_rm(root,max_files_per_dir,file_counter,pattern)
                        root_file_counter+=files_left
                        
                else:
                        root_file_counter+=file_counter

        #ask
        if run_number!='':
            sys.stdout.write("Finished second truncate run on given root directory. Current counted files:"+str(root_file_counter)+"\n")
            sys.exit(2)            
        
        if root_file_counter > max_files_root_dir:
            sys.stdout.write("Starting second run on root directory with 2x lower requirements. Current counted files in root:"+str(root_file_counter)+"\n")            
            check_directory_files_trunc(directory,max_files_per_dir/2,max_age/2,max_size/2,pattern,max_files_root_dir,2)                        




def check_directory_files_partial_trunc(directory,max_files_per_dir,max_size,pattern,max_files_root_dir,truncate_size_to):
        """Check directory files recursively if they match the given pattern.\n
       If they do get their size and compare them with given limits.\n
       Partly truncates a file if necessary."""
        
        for root, directories, filenames in os.walk(directory):
                for file in fnmatch.filter(filenames, pattern):
                    path=root+"/"+file
                    file_size = str(os.path.getsize(path))
                    
                    if(int(file_size)>int(max_size)):
                            partly_truncate_file(path,truncate_size_to,file_size)

                                   
def filesystem_type(path):
    """Uses disk_partitions() from psutil to check what fs the given directory is"""
    root_type = ""
    for part in disk_partitions():
        if part.mountpoint == '/':
            root_type = part.fstype
            continue

        if mypath.startswith(part.mountpoint):
            return part.fstype

    return root_type


    
                    
def main():
    #try:
        parser = argparse.ArgumentParser(description='Log cleaner') 
        parser.add_argument('-max_size', nargs='?',type=str,default=100000000000,help="maximum file size in bytes, defaults to 100gb if not specified. accepts bytes or mb (X or XMB)")
        parser.add_argument('-directory',type=str,default=". The directory parameter is required and passed with -directory",help="Required argument. Root directory from which to begin procedure recursively")
        parser.add_argument('-file_type',type=str,default="*",help="Which files to operate on accepts a shell glob, defaults to * if not specified")
        parser.add_argument('-operation',type=str,default="ls",help="rm/trunc/ls/partial_trunc, defaults to ls")
        parser.add_argument('-max_age',type=str,default="31390000",help="Maximum age of a file in seconds, defaults to 1 year. Accepts seconds(default) minutes or hours (Xm or Xh)")
        parser.add_argument('-max_files_per_dir',type=int,default="10000",help="Maximum amount of files in a directory, defaults to 10000")
        parser.add_argument('-max_files_root_dir',type=int,default="50000",help="Maximum amount of files in the given root directory and all subdirectories, defaults to 50000")
        parser.add_argument('-truncate_size_to',type=str,default="256000000",help="When truncating a log file from the beginning, leave the last X bytes of the file, defaults to 256mb, default accepts bytes, also accepts megabytes")
        
        arg = parser.parse_args()

        #QOL formatting:
        if(str(arg.max_size).lower().endswith("mb")):
            arg.max_size = int(arg.max_size[:-2]) *1000000
            
        if(arg.max_age.lower().endswith("m")):
            arg.max_age = int(arg.max_age[:-1]) *60
            
        if(arg.max_age.lower().endswith("h")):
            arg.max_age = int(arg.max_age[:-1]) *3600
            
        if(arg.truncate_size_to.lower().endswith("mb")):
            arg.truncate_size_to = int(arg.truncate_size_to[:-2]) *1000000

        if int(arg.max_size) < 0.1:
            sys.stderr.write('Invalid maximum file size argument. Given is:'+str(arg.max_size)+"bytes. Required is: SIZE > 0\n")
            sys.exit(1)
            
        if not os.access(arg.directory, os.W_OK):
            sys.stderr.write("Unable to acces or have no write access to given directory: "+arg.directory+"\n")
            sys.exit(1)
            
        if int(arg.max_size) < 0.1:
            sys.stderr.write('Invalid maximum age argument. Given is:'+str(arg.max_size)+" Required is: SIZE > 0\n")
            sys.exit(1)

        if arg.max_files_per_dir < 0.1 or arg.max_files_root_dir < 0.1:
            sys.stderr.write('Invalid maximum files per dir argument. Given is:'+str(arg.max_files_per_dir)+" Required is: SIZE > 0\n")
            sys.exit(1)

        if arg.max_files_per_dir >= arg.max_files_root_dir:
            sys.stderr.write("Warning: Maximum files per dir shouldn't be larger than maximim files in root directory.\nThe default values are 10000 and 50000 respectively\n")
            
        if int(arg.truncate_size_to) < 0.1 or int(arg.truncate_size_to) >= int(arg.max_size):
            sys.stderr.write("Invalid truncate_size_to value\n")
            sys.exit(1)
        
        signal.signal(signal.SIGHUP,  terminateProcess)
        signal.signal(signal.SIGINT,  terminateProcess)
        signal.signal(signal.SIGQUIT, terminateProcess) 
        signal.signal(signal.SIGABRT, receiveSignal)
        signal.signal(signal.SIGTERM, terminateProcess)
        
        if(arg.operation=="ls"):
            sys.stdout.write("Starting with operation ls and pattern "+arg.file_type+"\n")
            check_directory_files_ls(arg.directory,arg.max_files_per_dir,arg.max_age,arg.max_size,arg.file_type,arg.max_files_root_dir)

            sys.exit(0)
            
        elif(arg.operation=="rm"):
            sys.stdout.write("Starting with operation rm, pattern: "+arg.file_type+"\n")
            check_directory_files_rm(arg.directory,arg.max_files_per_dir,arg.max_age,arg.max_size,arg.file_type,arg.max_files_root_dir)
            
            sys.exit(0)

        elif(arg.operation=="partial_trunc"):
            #option -p is compatible with XFS (since Linux 2.6.38), ext4 (since Linux  3.0),
            #Btrfs (since Linux 3.7) and tmpfs (since Linux 3.5). 
            if(filesystem_type(arg.directory)=="ext4"):
                sys.stdout.write("Starting with operation partial_trunc, pattern: "+arg.file_type+"\n")
                check_directory_files_partial_trunc(arg.directory,arg.max_files_per_dir,arg.max_size,arg.file_type,arg.max_files_root_dir,arg.truncate_size_to)
            else:
                sys.stderr.write("Partial truncate is not supproted for this filesystem\n")
            
            sys.exit(0)        
    
        elif(arg.operation=="trunc"):
            sys.stdout.write("Starting with operation trunc, pattern: "+arg.file_type+"\n")
            check_directory_files_trunc(arg.directory,arg.max_files_per_dir,arg.max_age,arg.max_size,arg.file_type,arg.max_files_root_dir)
            sys.exit(0)
            
        else:
            sys.stderr.write("Invalid operation selected. Valid operations are ls, rm and trunc\n")

        sys.exit(1)
    
main()
