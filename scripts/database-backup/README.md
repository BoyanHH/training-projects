/[-gzip_enabled]/ yes for enabled, everything else for disabled  
/[-backup_name]/         \~date\~.sql / \~dbname-date\~.sql or anything else.  
/[-backup_dir]/ will append hostname,dbname,and type of backup(weekly/monthly) automatically  
/[-db_name]/ -> one per line  
/[-interactive]/ -> yes will run pg_dump with -W (always with a password prompt) anything else will run pg_dump with -w (no password prompt, but will check .pgpass file if needed).   If database is mysql it will check ~.my.cnf for username and password.  
  
If it is a connection to a remote mysql db, the mysql server has to be listening on 0.0.0.0(all) or on the client specific ip. Again if a password is required it will not be passed with "-p" but ~.my.cnf will be checked automatically.

Example entries of ~.my.cnf:  
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
  
  
TODO:  
HIGH:  
-
MEDIUM:  
-mysql option for local db dump to remote machine
LOW:  
-verbose option  
