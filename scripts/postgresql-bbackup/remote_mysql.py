import subprocess
import os
import sys
import psutil
import datetime


def check_dependencies():
    """Checks for dependencies
       Mandatory dependencies are - mysqldump,mysqlshow,find,mkdir
       Non-mandatory - gzip"""
    try:

        if subprocess.call('/usr/bin/mysqldump > /dev/null 2>&1', shell=True) == 127:
            sys.stderr.write("ERROR:Missing dependancy: mysqldump")
            sys.exit(1)
            
        if subprocess.call('/usr/bin/mysqlshow > /dev/null 2>&1', shell=True) == 127:
            sys.stderr.write("ERROR:Missing dependancy: mysqlshow")
            sys.exit(1)         

        if subprocess.call('/usr/bin/find  > /dev/null 2>&1', shell=True) == 127:
            sys.stderr.write("ERROR:Missing dependancy: find")
            sys.exit(1)

        if subprocess.call('/bin/mkdir  > /dev/null 2>&1', shell=True) == 127:
            sys.stderr.write("ERROR:Missing dependancy: mkdir")
            sys.exit(1)        

        if not gzip_enabled!="yes":
            if subprocess.call('/bin/gzip -h > /dev/null 2>&1', shell=True) == 127: 
                sys.stderr.write("ERROR:Missing dependancy: gzip")
                sys.exit(1)                 

    except subprocess.CalledProcessError:
        sys.stderr.write("ERROR:Unable to check for dependencies")
        sys.exit(1)        

        
def check_if_db_exists(db_name,db_user,ip,port):
    
    command="/usr/bin/mysqlshow  -u "+db_user+" -h "+ip+" --port="+port+" "
    try:
         output = subprocess.check_output([command],shell=True, stderr=subprocess.PIPE).decode('utf-8')
    except subprocess.CalledProcessError:
        sys.stderr.write("ERROR:Unable to check if database exists: "+str(db_name)+". User or database does not exist\n")
        sys.exit(1)              
    if db_name not in output:
        sys.stderr.write("ERROR:Database does not exist: "+str(db_name)+ "\n")
        sys.exit(1)            


def check_directories(backup_dir_daily,backup_dir_weekly,backup_dir_monthly):
        """Checks if needed directories exist and are writeable"""
        command="/bin/mkdir -p "
        
        if not os.access(backup_dir_daily, os.W_OK):
            sys.stderr.write("WARNING:Cannot write to daily backupdir OR directory does not exist.\n "+backup_dir_daily+"\n")
            try:
                 daily_command=command+backup_dir_daily              
                 output = subprocess.check_output([daily_command],shell=True, stderr=subprocess.PIPE).decode('utf-8')

            except subprocess.CalledProcessError:
                sys.stderr.write("ERROR: Trying to create daily backup dir "+str(daily_command)+"\n")
                sys.exit(1)
                
        
        if not os.access(backup_dir_weekly, os.W_OK):
          sys.stderr.write("WARNING:Cannot write to weekly backupdir OR directory does not exist.\n "+backup_dir_daily+"\n")
          try:                 
                 weekly_command=command+backup_dir_weekly
                 output = subprocess.check_output([weekly_command],shell=True, stderr=subprocess.PIPE).decode('utf-8')                  

          except subprocess.CalledProcessError:
                sys.stderr.write("ERROR: Trying to create weekly backup dir "+str(weekly_command)+"\n")
                sys.exit(1)                  
            
        if not os.access(backup_dir_monthly, os.W_OK):
            sys.stderr.write("WARNING:Cannot write to weekly backupdir OR directory does not exist.\n "+backup_dir_daily+"\n")
            try:
                 monthly_command=command+backup_dir_monthly
                 output = subprocess.check_output([monthly_command],shell=True, stderr=subprocess.PIPE).decode('utf-8')                  
            except subprocess.CalledProcessError:
                sys.stderr.write("ERROR: Trying to create monthly backup dir "+str(monthly_command)+"\n")
                sys.exit(1)                  
            
            

def type_of_backup(weekly_backup_day,monthly_backup_date):
    time_now = datetime.datetime.now()
    current_day = time_now.strftime("%A")
    if current_day == weekly_backup_day:
        return "weekly"
    current_date = time_now.day
    
    if monthly_backup_date == str(current_date):
        return "monthly"
    
    return "daily"


def daily_backup_procedure(backup_dir_daily,days_expire_daily,db_name,backup_name,db_user,mysql_dump_cmd):
    command="/usr/bin/find "+backup_dir_daily+" -maxdepth 1 -type f -name \"*.sql*\" -mtime +"+days_expire_daily
    try:
             output = subprocess.check_output([command],shell=True, stderr=subprocess.PIPE).decode('utf-8')
    except subprocess.CalledProcessError:
            sys.stderr.write("ERROR: Failed to remove old daily backups ")
            sys.exit(1)              
    output_formatted=output.split('\n')
    
    try:
        for old_file in output_formatted[:-1]:
            os.remove(old_file)
            
    #except IsADirectoryError:
   #     sys.stderr.write(" File is a directory(unable to remove)= "+old_file)
    except FileNotFoundError:
        sys.stderr.write("WARNING: File not found= "+old_file+"when attempting to remove it")

    if not gzip_enabled!="yes":    
        mysql_dump_cmd+="| /bin/gzip > "+backup_dir_daily+"/"+backup_name

    else:
        mysql_dump_cmd+=" > "+backup_dir_daily+""+backup_name

    print(mysql_dump_cmd)

    try:
         output = subprocess.check_output([mysql_dump_cmd],shell=True, stderr=subprocess.PIPE).decode('utf-8')
    except subprocess.CalledProcessError:
        sys.stderr.write("ERROR:Failed to do daily backup \n")
        sys.exit(1)              #exit code fix later
    print("Successfull daily backup \n")
    return 0


def weekly_backup_procedure(backup_dir_weekly,days_expire_weekly,db_name,backup_name,db_user,mysql_dump_cmd):
    command="/usr/bin/find "+backup_dir_weekly+" -maxdepth 1 -type f -name \"*.sql*\" -mtime +"+days_expire_weekly
    try:
             output = subprocess.check_output([command],shell=True, stderr=subprocess.PIPE).decode('utf-8')
    except subprocess.CalledProcessError:
            sys.stderr.write("WARNING:Failed to remove old weekly backups \n")
            sys.exit(1)  #exit code fix later

    output_formatted=output.split('\n')
    try:
        for old_file in output_formatted[:-1]:
            os.remove(old_file)
            
    except FileNotFoundError:
        sys.stderr.write("WARNING: File not found="+old_file)

    try:         
        if not gzip_enabled!="yes":    
            mysql_dump_cmd+="| /bin/gzip > "+backup_dir_weekly+"/"+backup_name

        else:
            mysql_dump_cmd+=" > "+backup_dir_weekly+""+backup_name
        output = subprocess.check_output([mysql_dump_cmd],shell=True, stderr=subprocess.PIPE).decode('utf-8')         
    except subprocess.CalledProcessError:
        sys.stderr.write("ERROR: Failed to do weekly backup\n")
        sys.exit(1) 
    return 0


def monthly_backup_procedure(backup_dir_monthly,days_expire_monthly,db_name,backup_name,db_user,mysql_dump_cmd):
    command="/usr/bin/find "+backup_dir_monthly+" -maxdepth 1 -type f -name \"*.sql*\" -mtime +"+days_expire_monthly
    try:
             output = subprocess.check_output([command],shell=True, stderr=subprocess.PIPE).decode('utf-8')
    except subprocess.CalledProcessError:
            sys.stderr.write("ERROR: Failed to remove old monthly backups\n")
            sys.exit(1)  #exit code fix later
    
    output_formatted=output.split('\n')
    try:
        for old_file in output_formatted[:-1]:
            os.remove(old_file)

    except FileNotFoundError:
        sys.stderr.write("WARNING: File not found="+old_file)

    if not gzip_enabled!="yes":    
        mysql_dump_cmd="| /bin/gzip > "+backup_dir_monthly+"/"+backup_name
            

    else:
        mysql_dump_cmd+="> "+backup_dir_monthly+""+backup_name                
        
    try:
         output = subprocess.check_output([mysql_dump_cmd],shell=True, stderr=subprocess.PIPE).decode('utf-8')
    except subprocess.CalledProcessError:
        sys.stderr.write("ERROR: Failed to do monthly backup\n")
        sys.exit(1)              
    return 0

    
def main(config,database):
    #try:
        global gzip_enabled
        gzip_enabled = config["DEFAULT"]["gzip_enabled"]
        check_dependencies()

        hostname = config["DEFAULT"]["remote_ip"]
        backup_dir_daily = config["DEFAULT"]["backup_dir"]+hostname+"/"+database+"/daily"
        backup_dir_weekly = config["DEFAULT"]["backup_dir"]+hostname+"/"+database+"/weekly/"
        backup_dir_monthly = config["DEFAULT"]["backup_dir"]+hostname+"/"+database+"/monthly/"
            

        if(config["DEFAULT"]["interactive"]=="yes"):
            mysql_dump_cmd = "/usr/bin/mysqldump --user="+config["DEFAULT"]["db_user"]+" --port="+config["DEFAULT"]["remote_port"]+" --host="+config["DEFAULT"]["remote_ip"]+" -p "
        else:
            mysql_dump_cmd = "/usr/bin/mysqldump --user="+config["DEFAULT"]["db_user"]+ " "+"--port="+config["DEFAULT"]["remote_port"]+" --host="+config["DEFAULT"]["remote_ip"]

        mysql_dump_cmd+=" "+database+" "
        
        
        check_if_db_exists(database,config["DEFAULT"]["db_user"],config["DEFAULT"]["remote_ip"],config["DEFAULT"]["remote_port"])
        
        if(config["DEFAULT"]["backup_name"]=="~date~.sql"):
            backup_name = datetime.datetime.now().strftime("%d")+"-"+datetime.datetime.now().strftime("%m")+".sql"

        elif(config["DEFAULT"]["backup_name"]=="~dbname-date~.sql"):
            backup_name = database+"-"
            backup_name += datetime.datetime.now().strftime("%d")+"-"+datetime.datetime.now().strftime("%m")+".sql"

        else:
            backup_name = config["DEFAULT"]["backup_name"]
            if not (backup_name.endswith(".sql")):
                    backup_name += ".sql"

        if not gzip_enabled != "yes":
          if not (backup_name.endswith(".gz")):
            backup_name += ".gz"
            
        db_user = config["DEFAULT"]["db_user"]
        
        check_directories(backup_dir_daily,backup_dir_weekly,backup_dir_monthly)
        
        backup_type = type_of_backup(config["DEFAULT"]["weekly_backup_day"],config["DEFAULT"]["monthly_backup_date"])
        
        if backup_type == "daily":
            daily_backup_procedure(backup_dir_daily,config["DEFAULT"]["days_expire_daily"],database,backup_name,config["DEFAULT"]["db_user"],mysql_dump_cmd)
            return 0

        if backup_type == "weekly":
            weekly_backup_procedure(backup_dir_weekly,config["DEFAULT"]["days_expire_weekly"],database,backup_name,config["DEFAULT"]["db_user"],mysql_dump_cmd)
            daily_backup_procedure(backup_dir_daily,config["DEFAULT"]["days_expire_daily"],database,backup_name,config["DEFAULT"]["db_user"],mysql_dump_cmd)

            return 0
            
        else:
            monthly_backup_procedure(backup_dir_monthly,config["DEFAULT"]["days_expire_monthly"],database,backup_name,config["DEFAULT"]["db_user"],mysql_dump_cmd)

            daily_backup_procedure(backup_dir_daily,config["DEFAULT"]["days_expire_daily"],database,backup_name,config["DEFAULT"]["db_user"],mysql_dump_cmd)

            return 0
    #except:
     #   sys.stderr.write("CRITICAL:Main exception")
        
            
#try:
if __name__ == '__main__':
    main()
#except:
#   sys.stderr.write(" Main exception")
#   sys.exit(-1)
