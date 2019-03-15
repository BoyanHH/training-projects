import psutil
import subprocess
import os
import argparse
import sys
import configparser
from collections import OrderedDict
from pyzabbix.api import ZabbixAPI,ZabbixAPIException


def add_application(host_id,app_name,zapi):
    
    try:
            item = zapi.application.create(
                hostid=host_id,
                name=app_name,                
            )

    except ZabbixAPIException as e:
        if "already exists" in str(e):
            sys.stderr.write("Application "+app_name+" already exists\n")
            return -2
        return -2
    else:
        pass
        #print("Created app")

    for key,val in item.items():
        return(val)    
    sys.exit(1)


    
def add_items_to_application(host_id,app_name,zapi,app_id,hosts,master_item_id,information_parameters):

    id_of_app = [int(i) for i in app_id]
    
    for par in information_parameters:
        name=app_name+"_"+par
        val_type=3
        if(name.endswith("_state") or name.endswith("_percent") or name.endswith("_line")):
            val_type=4
        try:
            item = zapi.item.create(
                hostid=host_id,
                name=name,
                key_=name,
                type=18,            #18 means dependent item
                master_itemid=master_item_id,
                value_type=val_type,
                interfaceid=hosts[0]["interfaces"][0]["interfaceid"],
                preprocessing=[{"type":"5","params":name+"\s=\s(.*)\n\\1"}],
                applications=id_of_app,
            )
        except ZabbixAPIException as e:
            sys.stderr.write(e)
            sys.exit(1)            


    
def create_master_item(host_id,hosts,zapi):
    try:
                item = zapi.item.create(         ##item only has to be created once.
                hostid=host_id,
                name='get_service_info_master',
                key_='get_service_info[/etc/zabbix/zabbix_agentd.d/list_of_services]',
                type=0,
                value_type=4,
                interfaceid=hosts[0]["interfaces"][0]["interfaceid"],
                delay=300,
                )
    except ZabbixAPIException as e:
                #print(e)            
                #sys.exit()        
                return(zabb.get_id("item","get_service_info_master"))    #item was already created, maybe have this id in a conf file.
    else:
            return(item["itemids"][0])

def get_service_names_and_parameters(zapi,filename):   
    #try:
        current_services=[]
        information_parameters=[]
        temp_holder=[]
        params_are_ready=False
        with open(filename,'r') as file:
            content = file.read().splitlines()
            for word in content:
                if word.startswith('['):
                    current_services.append(word[1:-1])
                    temp_holder=[]
                else:
                    try:                        
                        temp_holder.append(word.split('.')[1])
                    except IndexError:
                        if(params_are_ready==False):
                            for word in temp_holder:
                                 information_parameters.append(str(word.split(' ')[0]).split('service_')[1])
                            params_are_ready=True
                            
            return current_services, information_parameters
    

            
def main():
    """main function that accepts arguemnts, runs the program and connects to zabbix server"""
    
    parser = argparse.ArgumentParser(description='Get information about systemd processes') ##gets argument(filename)
    parser.add_argument("host",type=str,help="addresss of zabbix server")
    parser.add_argument("user",type=str,help="zabbix user for login")
    parser.add_argument("password",type=str,help="zabbix user password")
    args = parser.parse_args()
    
    global zabb
    
    try:
        zabb = ZabbixAPI()
        zapi=ZabbixAPI(args.host,user=args.user,password=args.password)
        zapi.timeout=5.1
        
    except ZabbixAPIException as e:
        sys.stderr.write(e)
        sys.exit(1)
    #except :
        #sys.stderr.write("Unexpected error:"+str(sys.exc_info()[0]))
        #sys.exit(1)
        
    host_name = 'Zabbix server'
    hosts = zapi.host.get(filter={"host": host_name}, selectInterfaces=["interfaceid"])
    if hosts:
        host_id = hosts[0]["hostid"]
    
    master_item_id=create_master_item(host_id,hosts,zapi)
    
    processes,information_parameters= get_service_names_and_parameters(zapi,"/etc/zabbix/zabbix_agentd.d/boyans_service_monitoring/service_status.ini")

    for process in processes:
            print(process)
            exit_code_zac=add_application(host_id,process,zapi)
            if(exit_code_zac!=-2):
                add_items_to_application(host_id,process,zapi,exit_code_zac,hosts,master_item_id,information_parameters)
            
#try:
main()
#except:
 #       sys.stderr.write("Unexpected error:"+str(sys.exc_info()[0]))
  #      sys.exit(1)
        
