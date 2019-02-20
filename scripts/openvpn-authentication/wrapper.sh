#!/bin/bash -e

admin_crt="please_work3"
err_code=3
log_file="/var/log/openvpn_security.log"
#add err_log
if [ "$common_name" == "$admin_crt" ];then
	echo "admin_con_allowed admin_crt=$admin_crt">>$log_file
	exit 0
fi

return_value=source /etc/openvpn/script.sh $@ >> $log_file 2>>$err_log
#moje custom err da sa nad 1000 i da proverqvame za tqh
if [ $return_value==0 ];then
	echo "result=allow">>$log_file
	exit $return_value
fi
exit $err_code
