import subprocess
import os
import sys
import psutil
import datetime


#TODO: add error codes, fix names
#password?

def check_dependencies():
    """Checks for dependencies
       Mandatory dependencies are - pg_dump,psql,find,mkdir
       Non-mandatory - gzip """
    try:

        if subprocess.call('/usr/bin/pg_dump > /dev/null 2>&1', shell=True) == 127:
            sys.stderr.write("Missing dependancy: pg_dump")
            sys.exit(1)
            
        if subprocess.call('/usr/bin/psql > /dev/null 2>&1', shell=True) == 127:
            sys.stderr.write("Missing dependancy: psql")
            sys.exit(1)         

        if subprocess.call('/usr/bin/find  > /dev/null 2>&1', shell=True) == 127:
            sys.stderr.write("Missing dependancy: find")
            sys.exit(1)

        if subprocess.call('/bin/mkdir  > /dev/null 2>&1', shell=True) == 127:
            sys.stderr.write("Missing dependancy: mkdir")
            sys.exit(1)        

        if not gzip_enabled!="yes":
            if subprocess.call('/bin/gzip -h > /dev/null 2>&1', shell=True) == 127: 
                sys.stderr.write("Missing dependancy: gzip")
                sys.exit(1)                 

    except subprocess.CalledProcessError:
        sys.stderr.write(" Unable to check for dependencies")
        sys.exit(1)        #fix exit code

        
def check_if_db_exists(db_name,db_user): 
    command="/usr/bin/psql template1 -U "+db_user+" -c \"SELECT 1 AS result FROM pg_database WHERE datname='"+db_name+"'\""
    #ako e s parola -psqlrc ako e bez parola dase logva #??ask
    try:
         output = subprocess.check_output([command],shell=True, stderr=subprocess.PIPE).decode('utf-8')
         output = output.lstrip()
    except subprocess.CalledProcessError:
        sys.stderr.write(" Error accessing database "+str(db_name))
        sys.exit(1)              
    if "1" not in output:
        sys.stderr.write("Database does not exist. "+str(db_name))
        sys.exit(1)            #exit code fix later


def check_directories(backup_dir_daily,backup_dir_weekly,backup_dir_monthly):
        """Checks if needed directories exist and are writeable"""
        command="/bin/mkdir -p "
        
        if not os.access(backup_dir_daily, os.W_OK):
            sys.stderr.write("Cannot write to daily backupdir/directory does not exist.\n "+backup_dir_daily)
            try:
                 print("Attempting to create directory")
                 daily_command=command+backup_dir_daily              
                 output = subprocess.check_output([daily_command],shell=True, stderr=subprocess.PIPE).decode('utf-8')

            except subprocess.CalledProcessError:
                sys.stderr.write(" Error trying to create daily backup dir "+str(daily_command))
                sys.exit(1)
                
        
        if not os.access(backup_dir_weekly, os.W_OK):
          try:
                 print("Attempting to create directory")
                 weekly_command=command+backup_dir_weekly
                 output = subprocess.check_output([weekly_command],shell=True, stderr=subprocess.PIPE).decode('utf-8')                  

          except subprocess.CalledProcessError:
                sys.stderr.write(" Error trying to create weekly backup dir "+str(weekly_command))
                sys.exit(1)                  
            
        if not os.access(backup_dir_monthly, os.W_OK):
            try:
                 print("Attempting to create directory")
                 monthly_command=command+backup_dir_monthly
                 output = subprocess.check_output([monthly_command],shell=True, stderr=subprocess.PIPE).decode('utf-8')                  
            except subprocess.CalledProcessError:
                sys.stderr.write(" Error trying to create monthly backup dir "+str(monthly_command))
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


def daily_backup_procedure(backup_dir_daily,days_expire_daily,db_name,backup_name):
    command="/usr/bin/find "+backup_dir_daily+" -maxdepth 1 -type f -name \"*.sql*\" -mtime +"+days_expire_daily
    try:
             output = subprocess.check_output([command],shell=True, stderr=subprocess.PIPE).decode('utf-8')
    except subprocess.CalledProcessError:
            sys.stderr.write(" Failed to remove old daily backups")
            sys.exit(1)              
    output_formatted=output.split('\n')

    try:
        for old_file in output_formatted[:-1]:
            os.remove(old_file)
            
    except IsADirectoryError:
        sys.stderr.write("File is a directory(unable to remove)="+old_file)
    except FileNotFoundError:
        sys.stderr.write("File not found="+old_file)
    if not gzip_enabled!="yes":    
        command="/usr/bin/pg_dump -Fp -U postgres "+db_name+" | /bin/gzip > "+backup_dir_daily+"/"+backup_name
    else:
        command="/usr/bin/pg_dump -Fp -U postgres "+db_name+" > "+backup_dir_daily+""+backup_name
        print(command)

    try:
         output = subprocess.check_output([command],shell=True, stderr=subprocess.PIPE).decode('utf-8')
    except subprocess.CalledProcessError:
        sys.stderr.write(" Failed to do daily backup")
        sys.exit(1)              #exit code fix later

    print("Successfull daily backup")
    return 0

def weekly_backup_procedure(backup_dir_weekly,days_expire_weekly,db_name,backup_name):
    command="/usr/bin/find "+backup_dir_weekly+" -maxdepth 1 -type f -name \"*.sql*\" -mtime +"+days_expire_weekly
    try:
             output = subprocess.check_output([command],shell=True, stderr=subprocess.PIPE).decode('utf-8')
    except subprocess.CalledProcessError:
            sys.stderr.write(" Failed to remove old weekly backups")
            sys.exit(1)  #exit code fix later

    output_formatted=output.split('\n')
    try:
        for old_file in output_formatted[:-1]:
            os.remove(old_file)
            
    except IsADirectoryError:
        sys.stderr.write("File is a directory(unable to remove)="+old_file)
    except FileNotFoundError:
        sys.stderr.write("File not found="+old_file)
    if not gzip_enabled!="yes":    
        command="/usr/bin/pg_dump -Fp -U postgres "+db_name+" | /bin/gzip > "+backup_dir_weekly+"/"+backup_name
    else:
        command="/usr/bin/pg_dump -Fp -U postgres "+db_name+" > "+backup_dir_weekly+""+backup_name
        print(command)
    try:
         output = subprocess.check_output([command],shell=True, stderr=subprocess.PIPE).decode('utf-8')
    except subprocess.CalledProcessError:
        sys.stderr.write(" Failed to do weekly backup")
        sys.exit(1)              #exit code fix later

    print("Successfull weekly backup at "+backup_dir_weekly)
    return 0


def monthly_backup_procedure(backup_dir_monthly,days_expire_monthly,db_name,backup_name):
    command="/usr/bin/find "+backup_dir_monthly+" -maxdepth 1 -type f -name \"*.sql*\" -mtime +"+days_expire_monthly
    try:
             output = subprocess.check_output([command],shell=True, stderr=subprocess.PIPE).decode('utf-8')
    except subprocess.CalledProcessError:
            sys.stderr.write(" Failed to remove old monthly backups")
            sys.exit(1)  #exit code fix later

    output_formatted=output.split('\n')
    try:
        for old_file in output_formatted[:-1]:
            os.remove(old_file)
            
    except IsADirectoryError:
        sys.stderr.write("File is a directory(unable to remove)="+old_file)
    except FileNotFoundError:
        sys.stderr.write("File not found="+old_file)
    if not gzip_enabled!="yes":    
        command="/usr/bin/pg_dump -Fp -U postgres "+db_name+" | /bin/gzip > "+backup_dir_monthly+"/"+backup_name
    else:
        command="/usr/bin/pg_dump -Fp -U postgres "+db_name+" > "+backup_dir_monthly+""+backup_name
    try:
         output = subprocess.check_output([command],shell=True, stderr=subprocess.PIPE).decode('utf-8')
    except subprocess.CalledProcessError:
        sys.stderr.write(" Failed to do weekly backup")
        sys.exit(1)              #exit code fix later
    print("Successfull monthly backup")
    return 0

def get_hostname():
    command="/bin/hostname"
    try:
            output = subprocess.check_output([command],shell=True, stderr=subprocess.PIPE).decode('utf-8')
    except subprocess.CalledProcessError:
            sys.stderr.write(" Failed to aquire hostname from command:"+command)
            sys.exit(1)              
    return output[:-1]
    
def main(config,database):
    hostname=get_hostname()
    backup_dir_daily = config["DEFAULT"]["backup_dir"]+hostname+"/"+database+"/"
    backup_dir_weekly = config["DEFAULT"]["backup_dir"]+hostname+"/"+database+"/weekly/"
    backup_dir_monthly = config["DEFAULT"]["backup_dir"]+hostname+"/"+database+"/monthly/"
         
    global gzip_enabled
    gzip_enabled = config["DEFAULT"]["gzip_enabled"]

    check_dependencies()

    if(config["DEFAULT"]["backup_name"]=="date.sql"):
        backup_name     = datetime.datetime.now().strftime("%d")+"-"+datetime.datetime.now().strftime("%m")+".sql"

    elif(config["DEFAULT"]["backup_name"]=="dbname-date.sql"):
        backup_name=database+"-"
        backup_name     += datetime.datetime.now().strftime("%d")+"-"+datetime.datetime.now().strftime("%m")+".sql"

    else:
        backup_name = config["DEFAULT"]["backup_name"]
        if not (backup_name.endswith(".sql")):
                backup_name+=".sql"

    if not gzip_enabled!="yes":
      if not (backup_name.endswith(".gz")):
        backup_name+=".gz"
    
    check_if_db_exists(database,config["DEFAULT"]["db_user"])  
    check_directories(backup_dir_daily,backup_dir_weekly,backup_dir_monthly)
    backup_type = type_of_backup(config["DEFAULT"]["weekly_backup_day"],config["DEFAULT"]["monthly_backup_date"])
    
    if backup_type == "daily":
        daily_backup_procedure(backup_dir_daily,config["DEFAULT"]["days_expire_daily"],database,backup_name)
        return 0

    if backup_type == "weekly":
        weekly_backup_procedure(backup_dir_weekly,config["DEFAULT"]["days_expire_weekly"],database,backup_name)
        return 0
        
    else:
        monthly_backup_procedure(backup_dir_monthly,config["DEFAULT"]["days_expire_monthly"],database,backup_name)
        return 0
        
            
#try:
if __name__ == '__main__':
    main()
#except:
 #   sys.stderr.write(" Main exception")
 #   sys.exit(-1)
