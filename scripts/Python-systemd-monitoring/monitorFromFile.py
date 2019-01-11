import psutil
import subprocess
import os
import argparse
from subprocess import PIPE


def getProcessNames(filename):
    num_lines = sum(1 for line in open(filename))
    with open(filename,'r') as file:
        content=file.read() 
    processNames=content.split('\n')
    return processNames
    
def getPID(processName):
    command="systemctl status "+processName
    command+=" |grep PID:"
    try:
        output=subprocess.check_output([command], shell=True, stderr=PIPE)
    except subprocess.CalledProcessError:
        exit("No such process Exists")
    output=output.split(" ")
    return output[3]

def getStatus(processName):
    command="systemctl status "+processName
    command+=" |grep Active:"
    output=subprocess.check_output([command], shell=True, stderr=PIPE)
    output=output.split("Active:")
    return output[1]

def getPSUTILinfo(PID):
    p=psutil.Process(PID)
    print("INFORMATION FROM PSUTIL")
    print("Status:"+str(p.status()))
    print("%CPU(1s interval): "+str(p.cpu_percent(interval=1.0)))
    print("CPU times: "+str(p.cpu_times()))
    print("%memory used: "+str(p.memory_percent()))
    #NEEDS ROOT
    print("memory fullinfo: "+str(p.memory_full_info()))
    print("IO: "+str(p.io_counters()))
    #NEEDS ROOT ^
    print("Amount of threads: "+str(p.num_threads()))
    print("")

def getTOPinfo(PID):
    command="top -p"+PID+" -b -n 1 | tail -n1"
    output=subprocess.check_output([command], shell=True, stderr=PIPE)
    output=output.split("  ")
    print("INFORMATION FROM TOP")
    print("%CPU: "+str(output[9]))
    print("%MEM: "+str(output[10]))
    print("CPU time used: "+str(output[11]))
    print("")

def amountOfChildProcesses(PID):
    command="systemctl status "+processName
    command+=" |grep Tasks:"
    output=subprocess.check_output([command], shell=True, stderr=PIPE)
    output=output.split(" ")
    return output[5]
##----------------START-----------------
    
##get arguments(file name)    
parser=argparse.ArgumentParser(description='Get information about systemd processes')
parser.add_argument('filename')
args=parser.parse_args()
##read the file and get service 
processNames=getProcessNames(args.filename)
processNumber=0


while processNumber<len(processNames)-1:
    print("-----------------------------------------------------")
    processName=str(processNames[processNumber])
    print("Process name: "+processName)
    PID=getPID(processName)
    print("PID: "+PID)
    status=getStatus(processName)
    print("Status(systemctl): "+status)
    if "running" in status:
        getPSUTILinfo(int(PID))
        getTOPinfo(PID)    
        print("Tasks(from systemctl): "+str(amountOfChildProcesses(int(PID))))

    processNumber+=1
