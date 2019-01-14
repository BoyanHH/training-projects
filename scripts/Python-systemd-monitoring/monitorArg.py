import psutil
import subprocess
import os
import argparse                                                                                  
from subprocess import PIPE 


def checkDependancies():
    """Checks for dependencies"""
    if subprocess.call('grep > /dev/null 2>&1', shell=True)==127:
        print("Missing dependancy: grep")
        exit(3)
    if subprocess.call('systemctl > /dev/null 2>&1', shell=True)==127:##!=0 ?
        print("Missing dependancy: systemctl")
        exit(2)


def getProcessNames(filename):
    """Opens the file(that is an argument when running the program), reads the file, and splits by newline """
    try:
        num_lines = sum(1 for line in open(filename))
        with open(filename,'r') as file:
            content=file.read()
    except IOError:
        print("Could not read file: "+str(filename))        
        exit(4)
    processNames=content.split('\n')
    return processNames
    

def getPID(processName):
    """Uses systemctl show to get PID, if no PID is available checks if service is loaded/inactive/not-found"""
    command="systemctl show "+processName
    command+=" -p MainPID"
    try:
        output=subprocess.check_output([command], shell=True, stderr=PIPE)
    except subprocess.CalledProcessError:
        try:
            command="systemctl --all --type service "
            command+="|grep "
            command+=processName
            output=subprocess.check_output([command], shell=True, stderr=PIPE)
        except subprocess.CalledProcessError:
            print("No such process Exists: "+str(processName))
            return False;
        if "inactive" in output:
            if "not-found" in output:
                print("Process "+str(processName)+" is inactive and CAN'T BE FOUND")
                return False;
            print("Process "+str(processName)+" is inactive but loaded")
            return False;
        else:
            print("No such process Exists: "+str(processName))
            return False;
        
    output=output.split("=")
    if(output[1]=="0\n"):
        print("No such process Exists: "+str(processName))
        return False;
    return output[1]


def getStatus(processName):
    """Uses systemctl status PROCESSNAME to get information about when process was started(how long ago) """
    ##ne e nujen try i except za CalledProcessError?
    command="systemctl status "+processName
    command+=" |grep Active:"
    output=subprocess.check_output([command], shell=True, stderr=PIPE)
    output=output.split("Active:")
    return output[1]


def getPSUTILinfo(PID):
    """Uses psutil to get status, CPU info, memory info, io info, amount of threads and CMDL that called the process"""
    try:
        p=psutil.Process(PID)
        print("###INFORMATION FROM PSUTIL###\n")
        print("Status="+str(p.status()))
        print("%CPU(.45s interval)="+str(p.cpu_percent(interval=0.45)))

        print("###CPU TIMES:###")        
        cpuTimes=str(p.cpu_times())        
        cpuTimes=cpuTimes[10:-1]
        cpuTimes=cpuTimes.split(", ")
        for x in range(4):
            print(cpuTimes[x])
        
        print("%memory used="+str(p.memory_percent()))
        print("Command line that called process="+str(p.cmdline()))

        #NEEDS ROOT###########################
        print("###Full memory Info:###")
        memInfo=str(p.memory_full_info())
        memInfo=memInfo[9:-1]
        memInfo=memInfo.split(", ")
        for x in range(10):
            print(memInfo[x])
        #######################################
        print("###IO Info:###")            
        IOinfo=str(p.io_counters())
        IOinfo=IOinfo[4:-1]
        IOinfo=IOinfo.split(", ")
        for x in range(4):
            print(IOinfo[x])
        #NEEDS ROOT ^
        print("")
        print("Amount of threads="+str(p.num_threads()))
    except psutil.AccessDenied:
        print("Need root access(psutil) for process PID="+str(PID))
        
def amountOfChildProcesses(PID):
    """Uses systemctl show to get the amount of chlid processes (TasksCUrrent)"""
    command="systemctl show "+processName
    command+=" -p TasksCurrent"
    output=subprocess.check_output([command], shell=True, stderr=PIPE)
    return output
##----------------START--------------------
checkDependancies()
##get arguments(file name)    
parser=argparse.ArgumentParser(description='Get information about systemd processes')
parser.add_argument('filename')
args=parser.parse_args()
##read the file and get the processNames
processNames=getProcessNames(args.filename)
processNumber=0

while processNumber<len(processNames)-1:
    PID=False
    while(PID==False):
        print("-----------------------------------------------------")
        processName=str(processNames[processNumber])
        if(processName==""):
            exit("No more processes")
        print("Process name: "+processName)
        PID=getPID(processName)
        if(PID==False):
            processNumber+=1
    
    print("PID="+str(PID))
    status=getStatus(processName)
    print("Status(systemctl)="+status)
    if "running" in status:
        getPSUTILinfo(int(PID))
        print((amountOfChildProcesses(int(PID))))

    processNumber+=1
