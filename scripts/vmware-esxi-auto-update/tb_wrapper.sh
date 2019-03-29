#!/bin/bash -e	

#TODO:
#user friendly messages.


configfile="wrapper.conf"
declare -A config        #array used for reading configuration file.

cat="/bin/cat"
touch="/usr/bin/touch"
ssh="/usr/bin/ssh"

esxi_host_addr_file="/home/boyan/file_with_ip"
esxi_user="root"

ssh_get_ESXI_ip_cmd="$cat $esxi_host_addr_file"
ssh_firewall_cmd="esxcli network firewall ruleset set -e true -r httpClientd"
ssh_update_cmd="esxcli software profile update -p ESXi-6.0.0-20181104001-standard -d https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml --force"


if [[ ! -e "$configfile" ]]; then
	echo "Error: Configuration file does not exist. It must be present in script directory"
	exit 1

while read line
do
    if echo $line | grep -F = &>/dev/null
    then
        varname=$(echo "$line" | cut -d '=' -f 1)
	echo $varname
        config[$varname]=$(echo "$line" | cut -d '=' -f 2)
    fi
done < $configfile

user=${config[user]}
host=${config[host]}
ssh_port=${config[port]}

exit 1

#check if err log exists, if not create it.
if [[ ! -e "$err_dir$err_log_name" ]]; then
    mkdir -p "$err_log_dir"		#built-in bash cmd
    $touch "$err_log_dir$err_log_name"
fi

#get the needed ip address from the file($ip_location)
esxi_ip="$($ssh $user@$host -p$ssh_port $ssh_get_ESXI_ip_cmd)"

$ssh $esxi_user@$esxi_ip -p$ssh_port $ssh_firewall_cmd 

$ssh $esxi_user@$esxi_ip -p$ssh_port $ssh_update_cmd

echo "Finished."



