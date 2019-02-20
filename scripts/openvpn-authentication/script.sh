#!/bin/bash 

date_cmd="$(/bin/date "+%F %T")"
err_log="/var/log/openvpn_security_err.log"
file_name="/etc/openvpn/security_file"
echo_cmd="/bin/echo -n"
openvpn_log="/var/log/openvpn.log"
ip_size=5

if [ ! -f $err_log ];then
	echo "WARNING=UNABLE TO ACCESS ERROR LOG">>$openvpn_log
	#exit 1001
fi


if [ ! -f $file_name ];then
	echo "$date_cmd ERROR=SECURITY_FILE_DOES_NOT_EXIST">>$err_log 
	exit 0 #allow everyone if there is no file
fi


crt_from_file=$(/bin/cat "$file_name" | cut -d "=" -f1)
ip_from_file=$(/bin/cat "$file_name" | cut -d "=" -f2)


for arg in "$@"
do
if [ "$arg" == "-v" ] || [ "$arg" == "--verbose" ];then
	verbose="enabled"
	$echo_cmd "$date_cmd conn_from trusted_ip=${trusted_ip} common_name=${common_name} ip_from_file=$ip_from_file common_name=$crt_from_file "
fi
done


for ((x=1;x<$ip_size;x++));
do

ip_addr_check=$(echo $ip_from_file | cut -d "." -f$x)
real_ip=$(echo $trusted_ip | cut -d "." -f$x)

if [ "$ip_addr_check" == "" ];then
	exit 0
fi

if [ ! "$ip_addr_check" == "$real_ip" ];then
	if [ $verbose == "enabled" ];then echo "result=deny"
	fi
exit 4
fi
done

exit 0 #allow all if incorrect security_file

