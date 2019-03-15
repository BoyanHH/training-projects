*Scripts are called by name, .py files should not be changed*  
  
Example configuration:  
[DEFAULT]  
	;specify db names, one per line  
db_name            = second_test  
		     test_only  
		     no_perm  
		     dada  
  
	;specify main backup directory  
	;needed subdirectories (/daily/dbname, /weekly etc.)  
	;will be created automatically.  
backup_dir	   = /home/boyan/  
  
	;specify backup name. .sql and .gz can be added automatically  
	;use ~date~ or ~dbname-date~ for built-in auto replacement  
backup_name        = ~date~.sql  
  
	;Day on which backups will be put in /weekly/ directory  
weekly_backup_day  = Wednesday  
  
	;Date on which backups will be put in /monthly/ directory  
monthly_backup_date= 9  
  
	;backups onlder than specified days will be deleted(different for each dir.)  
days_expire_daily  = 100   
days_expire_weekly = 2  
days_expire_monthly = 5  
  
	;db user for the database  
db_user = postgres  
  
	;db type "mysql" or "postgresql"  
backup_db_type = postgresql  
  
	;whether to use gzip or not  
gzip_enabled = yes  
  
	;interctive password prompts(bad for automatic use)  
	;will NOT ask for ssh password. It will still use   
	;ket based authentication.  
	;If you have a .pgpass file it will use it and won't ask for a password.  
interactive = no  
  
	;is db on a remote location "yes" or "no"  
remote_db = no  
  
	;will the backup be done remotely(dump file will be on a different machine) "yes" or "no"  
backup_remotely = yes  
   
	;user ip and port for ssh  
remote_user = boyan  
remote_port = 22  
remote_ip = 192.168.1.123  
  
Options are:  
/[-gzip_enabled]/ yes for enabled, everything else for disabled  
/[-backup_name]/         \~date\~.sql / \~dbname-date\~.sql or anything else.  
/[-backup_dir]/ will append hostname,dbname,and type of backup(weekly/monthly) automatically  
/[-db_name]/ -> one per line  
**/[-interactive]/ -> yes will run pg_dump with -W (always with a password prompt) anything else will run pg_dump with -w (no password prompt, but will check .pgpass file if needed).   If database is mysql it will check ~.my.cnf for username and password.**
  
**If it is a connection to a remote mysql db, the mysql server has to be listening on 0.0.0.0(all) or on the client specific ip. Again if a password is required it will not be passed with "-p" but ~.my.cnf will be checked automatically.**  

**Example entries of ~.my.cnf:**
[command]  
#config to use with command  
[mysql]  
user=USERNAME  
password=PASSWORD  
[mysqlshow]            
user=USERNAME  
password=PASSWORD  
[mysqldump]           
user=USERNAME  
password=PASSWORD  

  
**Example entries of ~.pgpass**  
HOST:PORT:DBNAME:DBUSER:password  
localhost:5432:a_databse:a_user:user_password  
  
  
TODO:  
High:    
MEDIUM:  
-mysql option for local db dump to remote machine  
LOW:   
-verbose option  
