import sys
import subprocess

def check_conn_using_key(remote_ip,remote_port,remote_user,timeout):
    """Checks if ssh exists on local machine, if an ssh server exists on the
       remote machine and if a connection could be made.Accepted Parameters are
       remote ip,remote port,remote user,timeout"""
    timeout=str(timeout)
    try:
        ssh_check_cmd="ssh "+remote_user+"@"+remote_ip+" -p"+remote_port+" -o ConnectTimeout=5 -o PasswordAuthentication=no -o PubkeyAuthentication=yes exit"
        print("")
        if subprocess.call(ssh_check_cmd, shell=True) != 0:
            sys.stderr.write("Failed: ERROR:Unable to establish ssh connection\n")
            sys.exit(1)            
    except subprocess.CalledProcessError:
        sys.stderr.write("Failed: ERROR:Unable to check for ssh connection. Information:\n")
        sys.stderr.write(sys.exc_info()[0])
        sys.exit(1)
    return 0

        
def exec_single_command(remote_ip,remote_port,remote_user,cmd_ssh,ssh_type):
        main_ssh="ssh "+remote_user+"@"+remote_ip+" -p"+remote_port
        if(ssh_type==1):
            options_ssh= " -o ConnectTimeout=5 -o PasswordAuthentication=no -o PubkeyAuthentication=yes "
        command=main_ssh+options_ssh+" "+cmd_ssh
        try:         
            output = subprocess.check_output([command],shell=True).decode('utf-8')
        except subprocess.CalledProcessError:
            sys.stderr.write("ERROR: Unable to execute "+command+". Information:\n")
            sys.stderr.write(sys.exc_info()[0])        
            sys.exit(1) 
        return 0
