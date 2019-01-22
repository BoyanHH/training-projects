import psutil
import subprocess
import os
import argparse
import sys
import configparser

##############################
#Exit codes:
#3-missnig grep
#2-missing systemctl
#6-missing ps
#4-unable to read file(argument)-IOERROR
#7-unable to check for dependencies-subprocess.CalledProcessError
#8,9-process does not exist(user config file error)
#12 - no such process PSUTIL ERROR
#22 - ROOT ACCESS ERROR
#98-very bad --all --type service fgrep error
#99-base psutil exception-pstuil.Error
##############################

##############################
#Maybe add:
# memory_used from systemctl show
##############################psutil children amount
##############################

##############################//////////////
#TODO:
#   print format new style
################################## sys.exit instead of exit
################################## getPID rename and return all
################################## return dictionary at getPSUTILINFO
##################################for key, value in process_info.items():
##################################   https://docs.python.org/3/library/configparser.html
##################################add .service kogato go nqma v imeto pri print
##################################malki bukvi, _
##################################amount of child processes
##################################rename get_process_names = parse_config_file and check if services are valid
##################################loadState from systemctl show
##################################//////////////////

##############################
#TO ASK:
# https://stackoverflow.com/questions/36103448/convert-from-unix-timestamp-with-milliseconds-to-hhmmss-in-python vmesto ps -o etimes
#
#
#
#
#############################


def check_dependancies():
    """Checks for dependencies"""
    try:
        if subprocess.call('/bin/fgrep > /dev/null 2>&1', shell=True) == 127:
            print("Missing dependancy: grep")
            sys.exit(3)
        if subprocess.call('/bin/systemctl > /dev/null 2>&1', shell=True) == 127:##!=0 ?
            print("Missing dependancy: systemctl")
            sys.exit(2)
        if subprocess.call('/bin/ps -p 1 -o etimes > /dev/null 2>&1', shell=True) == 127:##!=0 ?
            print("Missing dependancy: ps")
            sys.exit(6)        
    except subprocess.CalledProcessError:
        print("Unable to check for dependencies")
        sys.exit(7)


def read_config_file(filename):
    """Opens the file(required argument when running the program), reads the file, splits by newline and executes check_config() """
    try:
        with open(filename,'r') as file:
            content=file.read().splitlines()
    except IOError:
        print("Could not read file="+filename)        
        sys.exit(4)
    return check_config(content)

    
def check_config(content):
    """checks if config contains valid service names with ||systemctl -- all --type service | fgrep PROCESSNAME||
    also appends .service if it's missing"""

    valid_process_names=[]
    for process_name in content:
        process = process_name.split(".")
        process[0] += str(".service" )
        command="systemctl --all --type service |fgrep \""+process[0]+"\" >/dev/null 2>&1"        
        try:
            output=subprocess.check_output([command], shell=True, stderr=subprocess.PIPE)
            if subprocess.call([command],shell=True)!=0:        #proverqva dali sushtestvuva takuv service, moje i direktno sus systemctl show komandata, no ne e tolkova sigurna(?)
                print(process[0]+" does not exist")            ## delete later
                sys.exit(8)                                    ## delete later
        except subprocess.CalledProcessError:
            print("Process "+process[0]+" does not exist")
            sys.exit(9);
        valid_process_names.append(process[0])
        
    return valid_process_names



def get_service_info(processName):

    """Uses systemctl show to get PID, if no PID is available checks if service is loaded/inactive/not-found"""

    command="systemctl show "+processName+" -p MainPID,ActiveState,SubState,LoadState"
    try:
        output=subprocess.check_output([command], shell=True, stderr=subprocess.PIPE)       
    except subprocess.CalledProcessError:
        print("systemctl --all --type service error="+str(processName)+"!!!VERY BAD!!!") ##TODO:ne e user friendly
        exit(98)

    output = output.decode('utf-8')
    output = output.split('=')
    PID=output[1].split('\n')
    
    parsable_output=[i.split('\n',1)[0] for i in output]       #formatirame lista, kato premahnem \n za po-lesen output
    
    config.add_section(processName)                            ##nova sekciq v configParser s imeto na procesa
    
    if(PID[0]!="0"):
        config.set(processName,"main_PID",parsable_output[1])  #samo ako PID ne e 0 dobavqme key:main_PID
    config.set(processName,"sub_state",parsable_output[3])
    config.set(processName,"service_state",parsable_output[4])
    config.set(processName,"load_state",parsable_output[2])
        
    return PID[0]              #vrushta PID na glavnata funkciq, izpolzva se za psutil.



def get_info_from_psutil(PID,processName):

    """Uses psutil to get status, CPU info, memory info, io info, amount of threads and CMDL that called the process"""
    
    try:
        command="ps -p "+str(PID)+" -o etimes"                             ##etimes vrushta uptime v sekundi, etime ima format HH-MM-SS        
        output=subprocess.check_output([command],shell=True, stderr=subprocess.PIPE).decode('utf-8')
        config.set(processName,"uptime_seconds",output[7:-1].lstrip())     ##7:-1, premahva purvite 7 simvola (vinagi sa ELAPSED) i posledniq, koito vinagi e \n
        
        p=psutil.Process(PID)

        config.set(processName,"amount_of_children",str(len(p.children())))
        config.set(processName,"cpu_0.45s_interval",str(p.cpu_percent(interval=0.45)))
        config.set(processName,"command_line",' '.join(p.cmdline()))
        config.set(processName,"amount_of_threads",str(p.num_threads()))
        
        memInfo=p.memory_full_info()
        
        config.set(processName,"memory_rrs_percent",str(p.memory_percent(memtype="rss")))
        config.set(processName,"memory_rss_bytes",str(memInfo.rss))
        config.set(processName,"nmemory_vms_bytes",str(memInfo.vms))
        config.set(processName,"memory_shared_bytes",str(memInfo.shared))
        config.set(processName,"memory_swap_bytes",str(memInfo.swap))

        IOinfo=p.io_counters()                          ##needs root
        
        config.set(processName,"io_read_count",str(IOinfo.read_count))
        config.set(processName,"io_write_count",str(IOinfo.write_count))
        config.set(processName,"io_read_bytes",str(IOinfo.read_bytes))
        config.set(processName,"io_write_bytes",str(IOinfo.write_bytes))
        
    except psutil.AccessDenied:
        print("Need root access(psutil) for process PID="+str(PID))
        sys.exit(22)
    except psutil.NoSuchProcess:
        print("No process found with PID="+str(PID))
        sys.exit(12)
    except psutil.Error:
        print("Base psutil exception\\\\\\\\very bad\\\\\\\\\\")            #TODO: something
        sys.exit(99)

def config_print(config):
    config.write(sys.stdout)                         ##shte printira sus space, za chetimost |dobavq se ,Fals|etu-
    
def main():
    check_dependancies()                             ##checks if systemctl, fgrep, ps exist     
    parser = argparse.ArgumentParser(description='Get information about systemd processes') ##gets argument(filename)
    parser.add_argument('filename', type=str)
    args = parser.parse_args()

    for process in read_config_file(args.filename):
        print("\n["+process+"]")            
        PID=get_service_info(process)                 ##getPID vrushta PID na procesa izpolzvaiki systemctl show
        if(PID!="0"):
            get_info_from_psutil(int(PID),process)
        config_print(config)
            
config=configparser.ConfigParser()        
main()
