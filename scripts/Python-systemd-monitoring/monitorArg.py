import psutil
import subprocess
import os
import argparse
import sys
import configparser

MISSING_DEPENDENCY_ERR = 3
FILE_IO_ERROR = 4
DEPENDENCY_CHECK_ERR= 8
NO_SUCH_PROCESS_ERR = 12
PSUTIL_BAD_PID_ERR=33
SYSTEMCTL_ALL_ERR=44
ROOT_PERMISSION_ERR = 22
SYSTEMCTL_SERVICE_ERR = 98
BASE_PSUTIL_ERROR = 99


def check_dependencies():    
    """Checks for dependencies"""
    
    try:
        if subprocess.call('/bin/systemctl > /dev/null 2>&1', shell=True) == 127:##!=0 ?
            print("Missing dependancy: systemctl")
            sys.exit(MISSING_DEPENDENCY_ERR)
            
        if subprocess.call('/bin/ps -p 1 -o etimes > /dev/null 2>&1', shell=True) == 127:##!=0 ?
            print("Missing dependancy: ps")
            sys.exit(MISSING_DEPENDENCY_ERR)
            
    except subprocess.CalledProcessError:
        print("Unable to check for dependencies")
        sys.exit(DEPENDENCY_CHECK_ERR)


def read_config_file(filename):
    """Opens the file(required argument when running the program), reads the file, splits by newline and executes check_config() """
    
    try:
        with open(filename,'r') as file:
            content = file.read().splitlines()
            
    except IOError:
        print("Could not read file=" + filename)        
        sys.exit(FILE_IO_ERROR)
        
    return check_config(content)

    
def check_config(content):
    """checks if config contains valid service names - runs systemctl --all --type service and saves it to an array \\
    also appends .service if it's missing"""
    
    valid_process_names = []    
    command = "systemctl --all --type service"
    
    try:
            output = subprocess.check_output([command], shell=True, stderr=subprocess.PIPE)
            
    except subprocess.CalledProcessError:
            print("Could not run systemctl --all --type service.")
            sys.exit(SYSTEMCTL_ALL_ERR);
            
    output = output.decode('utf-8')
            
    for process_name in content:
        process = process_name.split(".")
        process[0] += str(".service" )
        if process[0] in output:
            valid_process_names.append(process[0])
        else:
           print("No such process")
           exit(NO_SUCH_PROCESS_ERR)
           
    return valid_process_names


def get_service_info(processName):
    """Uses systemctl show to get PID, if no PID is available checks if service is loaded/inactive/not-found"""
    
    command = "systemctl show "+processName+" -p MainPID,ActiveState,SubState,LoadState"
    try:        
        output = subprocess.check_output([command], shell=True, stderr=subprocess.PIPE)
       
    except subprocess.CalledProcessError:
        print("systemctl --all --type service error="+str(processName)+"!!!VERY BAD!!!") ##TODO:ne e user friendly
        exit(SYSTEMCTL_SERVICE_ERR)
        
    output = output.decode('utf-8').split('=')
    PID = output[1].split('\n')
    
    parsable_output = [i.split('\n',1)[0] for i in output]     #formatirame lista, kato premahnem \n za po-lesen output
    
    service_info_dict={
            "main_PID":parsable_output[1],
            "sub_state":parsable_output[3],
            "service_state":parsable_output[4],
            "load_state":parsable_output[2]
        }


    return service_info_dict              


def get_info_from_psutil(PID,processName):
    """Uses psutil to get status, CPU info, memory info, io info, amount of threads and CMDL that called the process"""
    
    try:
        command = "ps -p "+str(PID)+" -o etimes | tail -n1" ##etimes vrushta uptime v sekundi, etime ima format HH-MM-SS
        
        output = subprocess.check_output([command],shell=True, stderr=subprocess.PIPE).decode('utf-8')

        proc = psutil.Process(PID)
        memory_info = proc.memory_full_info() 
        io_info = proc.io_counters()                          ##needs root
        
        info_from_psutil_dict={
            "amount_of_children":str(len(proc.children())),
            "cpu_usage_percent":str(proc.cpu_percent(interval=0.45)),
            "command_line":' '.join(proc.cmdline()),
            "amount_of_threads":str(proc.num_threads()),
            "uptime_seconds":output[0:-1].lstrip(),
            "memory_rrs_percent":str(proc.memory_percent(memtype="rss")),
            "memory_rss_bytes":str(memory_info.rss),
            "nmemory_vms_bytes":str(memory_info.vms),
            "memory_shared_bytes":str(memory_info.shared),
            "memory_swap_bytes":str(memory_info.swap),
            "io_read_count":str(io_info.read_count),
            "io_write_count":str(io_info.write_count),
            "io_read_bytes":str(io_info.read_bytes),
            "io_write_bytes":str(io_info.write_bytes)
        }
        
    except psutil.AccessDenied:
        print("Need root access(psutil) for process PID="+str(PID))
        sys.exit(ROOT_PERMISSION_ERR)
        
    except psutil.NoSuchProcess:
        print("No process found with PID="+str(PID))
        sys.exit(PSUTIL_BAD_PID_ERR)
        
    except psutil.Error:
        print("Base psutil exception\\\\\\\\very bad\\\\\\\\\\")            #TODO: something
        sys.exit(BASE_PSUTIL_ERROR)

        
    return info_from_psutil_dict


def config_build(config,service_info_dict,info_from_psutil_dict):
    """Builds config(used for otput) from service_info and info_from_psutil dictionaries"""
    
    for section in config.sections():
        for key in service_info_dict.keys():
            config.set(section,key,service_info_dict[key])
            
        if(service_info_dict.get("main_PID")== "0"):
            config.remove_option(section,"main_PID")        
            return
        
        for key in info_from_psutil_dict.keys():
            config.set(section,key,info_from_psutil_dict[key])

            
def config_print(config):
    """uses config.write to print output to sys.stdout"""
    
    config.write(sys.stdout)                         ##shte printira sus space, za chetimost |dobavq se ,False
    

def main():
    """main function that runs the program"""
    
    check_dependencies()                             ##checks if systemctl && ps exist     
    parser = argparse.ArgumentParser(description='Get information about systemd processes') ##gets argument(filename)
    parser.add_argument('filename', type=str,help="file that contains service names")
    args = parser.parse_args()
    
    for process in read_config_file(args.filename):
        config=configparser.ConfigParser()
        config.add_section(process)
        info_from_psuitl_dict = {}

        service_info_dict = get_service_info(process)##getPID vrushta PID na procesa izpolzvaiki systemctl show
        
        if(service_info_dict.get("main_PID")!= "0"):  ##ne iskame da vzimame psutil informaciq za proces, koito ne e running
            info_from_psutil_dict = get_info_from_psutil(int(service_info_dict.get("main_PID")),process)
            
        config_build(config,service_info_dict,info_from_psutil_dict)
        config_print(config)
            
try:
    main()
except:
    print("very bad")
    sys.exit(96)
