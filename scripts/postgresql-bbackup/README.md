-gzip_enabled yes for enabled, everything else for disabled
-backup_name         --date.sql / dbname-date.sql     or anything else.
-backup_dir will append hostname,dbname,and type of backup(weekly/monthly) automatically
-db_name -> one per line

[DEFAULT]
db_name            = test_only
		                 second_test
		                 dada
backup_dir	   = /var/test/
backup_name        = date.sql
weekly_backup_day  = Wednesday                         
monthly_backup_date= 14
days_expire_daily  = 15 
days_expire_weekly = 29
days_expire_monthly = 187
db_user = passuser
backup_type = local
backup_db_type = postgresql
gzip_enabled = yes
