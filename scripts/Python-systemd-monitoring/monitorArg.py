import psutil
import subprocess
import os
import argparse                                                                                  
from subprocess import PIPE 
##############################
#Exit codes:
#3-missnig grep
#2-missing systemctl
#6-missing ps
#4-unable to read file(argument)-IOERROR
#7-unable to check for dependencies-subprocess.CalledProcessError
#99-base psutil exception-pstuil.Error
#
##############################

##############################
#Maybe add:
## print("Uptime_seconds= "+str(p.create_time())) # The process creation time as a floating point number expressed in seconds since the epoch, in UTC. The return value is cached after first call.
## threads()    #Return threads opened by process as a list of named tuples including thread id and thread CPU times (user/system). On OpenBSD this method requires root privileges.
## connections(kind="inet") #Return socket connections opened by process as a list of named tuples. To get system-wide connections use psutil.net_connections(). Every named tuple provides 6 attributes:
# loadState from systemctl show
#
##############################

##############################
#TODO:
#Ln 80
#
#
##############################


def checkDependancies():
    """Checks for dependencies"""
    try:
        if subprocess.call('grep > /dev/null 2>&1', shell=True)==127:
            print("Missing dependancy: grep")
            exit(3)
        if subprocess.call('systemctl > /dev/null 2>&1', shell=True)==127:##!=0 ?
            print("Missing dependancy: systemctl")
            exit(2)
        if subprocess.call('ps -p 1 -o etimes > /dev/null 2>&1', shell=True)==127:##!=0 ?
            print("Missing dependancy: ps")
            exit(6)        
    except subprocess.CalledProcessError:
        print("Unable to check for dependencies")
        exit(7)


def getProcessNames(filename):
    """Opens the file(that is an argument when running the program), reads the file, and splits by newline """
    try:
        num_lines = sum(1 for line in open(filename))           ##moje i readlines(), no tova raboti sushto
        with open(filename,'r') as file:
            content=file.read()
    except IOError:
        print("Could not read file: "+str(filename))        
        exit(4)
    finally:
        file.close()
    processNames=content.split('\n')
    return processNames
    

def getPID(processName):
    """Uses systemctl show to get PID, if no PID is available checks if service is loaded/inactive/not-found"""

    command="systemctl show "+processName+" -p MainPID,TasksCurrent,ActiveState,SubState"
    try:
        output=subprocess.check_output([command], shell=True, stderr=PIPE)
        command="systemctl --all --type service |grep \""+processName+"\" >/dev/null 2>&1"        
        if subprocess.call([command],shell=True)!=0:        #proverqva dali sushtestvuva takuv service, moje i direktno sus systemctl show komandata, no ne e tolkova sigurna(?)
            print("Process "+processName+" does not exist")
            return False;  
    except subprocess.CalledProcessError:
        print("Process does not exist-systemctl --all --type service error="+str(processName)) ##TODO:ne e user friendly
        return False;

    output=output.split("=")
    PID=output[1].split('\n')
    zugzug=[i.split('\n',1)[0] for i in output]       #formatirame lista, kato premahnem \n za po-lesen output
    if(PID[0]=="0"):                                  #ako PID e 0, ili ne sushtestvuva izobshto ili ne e active
        if(zugzug[3]=="active"):
            print("process_state="+zugzug[3])
            print("sub_state="+zugzug[4]+"")
            return False;
        print("process_state="+zugzug[3])
        print("sub_state="+zugzug[4]+"")
        return False;

    print("main_PID="+zugzug[1])
    print("amount_of_child_processes="+zugzug[2])
    print("process_state="+zugzug[3])
    print("sub_state="+zugzug[4]+"")

    return PID[0]                       #vrushta PID na glavnata funkciq


def getPSUTILinfo(PID):
    """Uses psutil to get status, CPU info, memory info, io info, amount of threads and CMDL that called the process"""

    try:
        command="ps -p "+str(PID)+" -o etimes"             ##etimes vrushta uptime v sekundi, etime ima format HH-MM-SS        
        output=subprocess.check_output([command],shell=True, stderr=PIPE)
        print("uptime_seconds="+output[7:].lstrip())       ##7: to remove ELAPSED from the string

        p=psutil.Process(PID)

        print("cpu_0.45s_interval="+str(p.cpu_percent(interval=0.45)))
        print("command_line_that_called_process="+' '.join(p.cmdline()))

        print("memory_%_used="+str(p.memory_percent()))
        memInfo=p.memory_full_info()
        print("memory_rss="+str(memInfo.rss)+"\nmemory_vms="+str(memInfo.vms)+"\nmemory_shared="+str(memInfo.shared)+"\nmemory_swap="+str(memInfo.swap))
        
        IOinfo=p.io_counters()  
        print("io_read_count="+str(IOinfo.read_count)+"\nio_write_count="+str(IOinfo.write_count)+"\nio_read_bytes="+str(IOinfo.read_bytes)+"\nio_write_bytes="+str(IOinfo.write_bytes))
        #NEEDS ROOT ^
        print("amount_of_threads="+str(p.num_threads()))
        
    except psutil.AccessDenied:
        print("Need root access(psutil) for process PID="+str(PID))
    except psutil.NoSuchProcess:
        print("No process found with PID="+str(PID))
    except psutil.Error:
        print("Base psutil exception")
        exit(99)

##----------------START--------------------
        
checkDependancies()                             ##checks if systemctl and grep exist     
parser=argparse.ArgumentParser(description='Get information about systemd processes') ##gets argument(filename)
parser.add_argument('filename')
args=parser.parse_args()
processNames=getProcessNames(args.filename)     ##reads the file and returns an array of the process names
processNumber=0 

while processNumber<len(processNames)-1:        ##cikul, koito minava prez masiva s imena na procesi
    PID=False
    while(PID==False):                          ##PID vrushta false ako procesa ne e aktiven(nqma MainPID)
        processName=processNames[processNumber]
        if(processName==""):                    ##Ako procesa e ""-null-posledniq proces-nevaliden input
            exit("No more processes")
        print("\n["+processName+"]")            ##printira imeto na procesa
        PID=getPID(processName)                 ##getPID vrushta PID na procesa izpolzvaiki systemctl show
        if(PID==False):
            processNumber+=1                    ##PID vrushta false ako procesa ne e aktiven(nqma MainPID)
    
    if(PID!=False):
        getPSUTILinfo(int(PID))
        processNumber+=1
