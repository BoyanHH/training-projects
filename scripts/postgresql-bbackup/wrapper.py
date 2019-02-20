import subprocess
import os
import configparser
import argparse         #if needed later
import sys
import psutil
import datetime
#proverki,suboshteniq etc.
config = configparser.ConfigParser()
#####TO MAKE CONFIG FILE AN OPTION:
parser = argparse.ArgumentParser(description='Backup postgresql/mysql databases') ##gets argument(filename)
parser.add_argument('filename', type=str,help="config file with backup options")
args = parser.parse_args()
try:
    a=config.read(args.filename)
except configparser.Error:
    sys.stderr.write("CRITICAL: configparser error for config.read at:"+args.filename)
    exit(1)
#config.read("/var/backup/backup.conf")

for database in config.get("DEFAULT", "db_name").split("\n"):
        print("Using db: "+database)
        if(config["DEFAULT"]["backup_db_type"]=="postgresql"):
            import backup
            exit_value=backup.main(config,database)  ##postgresql
    
        #else:
        #   sql_backup.main()
