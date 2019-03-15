import psutil
import subprocess
import os
from subprocess import PIPE
processNumber=1
AmountOfProcesses=199


def getAllProcesses():
    output=subprocess.check_output(['systemctl list-units --type service'], shell=True, stderr=PIPE)
    return output

def getProcessInfo(output):
   global processNumber
   output=output.split('\n')
   return output[processNumber]

def getProcessName(processInfo):
    processName=processInfo.split(' ')
    return processName[0]

def isProcessActive(processInfo):
    if "active" in processInfo:
        return True
    else:
        return False
    
def isProcessRunning(processInfo):
    if "running" in processInfo:
       return True
    else:
       return False

def isProcessExited(processInfo):
    if "exited" in processInfo:
       return True
    else:
       return False
    
def getPID(processName):
    command="systemctl status "+processName
    command+=" |grep PID:"
    output=subprocess.check_output([command], shell=True, stderr=PIPE)
    output=output.split(" ")
    return output[3]
def allInformation(PID):
    PID=int(PID)
    print(PID)
    p=psutil.Process(PID)
    print("Process name:",p.name()," EXE: ",p.exe()," PID:",PID," PPID:",p.ppid()," Status:",p.status())

##TODO
    ##remove empty spaces in beginning
##----------------START-----------------
output=getAllProcesses()
while processNumber<40:
    processInfo=getProcessInfo(output)
    processName=getProcessName(processInfo)
    isActive=isProcessActive(processInfo)
    if isActive:
       ## print(processName)
        isRunning=isProcessRunning(processInfo)
        if isRunning:
            print(processName," is running")
            PID=getPID(processName)
            allInformation(PID)
            ##return CPU info
        elif isProcessExited(processInfo):
                print(processName, " is active but exited")
        else:
           print(processName, " is active but not running")
        
    else:
        print(processName, "is not active")
    
    processNumber+=1

