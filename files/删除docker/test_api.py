#!/usr/bin/python

import requests
import json
from datetime import *
import argparse

import re
import time
import json
import httplib
import urllib2

image_token = "12fd33018268c5e144da368af5085acde9319e34"
image_Authorization = "Token " + image_token

user_token = "3e49c0482d9675abb1d7c53daca2dc1333a25f08"
user_Authorization = "Token " + user_token

#username = "xyongcn@qq.com"
#password = "21b^54X3dafa2#37a"
username = "bitmoon@163.com"
password = "7kiYSglJk"

#username = "zhangrain911@163.com"
#password = "thumooc123"

headers = {
        "Content-Type": "application/json",
        "Authorization": image_Authorization,
        "username": username,
        "password": password
    }

base_url = "https://crl.ptopenlab.com:8800/restful/supernova"

#image_id = "2c61b3af-ec01-4409-9abd-d427680a6953"
#cluster_config_id = "43ba6f70-a49c-401f-8e72-b035b61387ef"
#test 79 dockers at a time

account_name = "test@qq.com"
account_pwd  = "password"

def create_user(account_name,account_pwd):
    headers = {
    "Content-Type": "application/json",
    "Authorization": user_Authorization
    }

    ret = requests.post("https://dashboard.ptopenlab.com:443/restful/supernova/user/register",
                        headers=headers, data=json.dumps({
                            "user_name": account_name,
                            "password": account_pwd,
                        }))
    print ret

def get_webshell(ip):
    headers = {
    "Content-Type": "application/json",
    "Authorization": user_Authorization
    }
    url = "https://dashboard.ptopenlab.com:443/restful/supernova/web_shell/get/Beijing/" + ip
    ret = requests.get(url,headers=headers)
    print ret.text

def cluster_config_create(image_id):
    url = base_url + "/cluster_config/create"

    body = json.dumps({                        
        "vms": [{"name": "edx_cluster_config", "image_id": image_id, 
	    "internal_ip": "40.40.40.10", "ext_enable": True},]
    })
    ret = requests.post(url,
                    headers=headers, data=body)

    print ret.text

def cluster_config_delete(cluster_config_id):
    url = base_url + "/cluster_config/delete/" + cluster_config_id
    ret = requests.delete(url,headers=headers)
    print ret.text

def cluster_create(cluster_config_id):
    url = base_url + "/cluster/create"
    body = json.dumps({                        
        "cluster_config_id": cluster_config_id,
        "cluster_number"   : 1,
    })
    ret = requests.post(url,headers=headers, data=body)
    print ret.text

def cluster_config_list():
    url = base_url + "/cluster_config/list"
    ret = requests.get(url,headers=headers)
    print ret.text

def cluster_list():
    url = base_url + "/cluster/list"
    ret = requests.get(url,headers=headers)
    ret = json.loads(ret.text)
    print ret["clusters"]

#only print status
def cluster_list_status():
    url = base_url + "/cluster/list"
    ret = requests.get(url,headers=headers)
    ret = json.loads(ret.text)
    return ret["clusters"]
    

def cluster_delete(cluster_id):
    url = base_url + "/cluster/delete/" + cluster_id
    print url
    ret = requests.delete(url,headers=headers)
    print ret.text
    
def cluster_show(cluster_id):
    url = base_url + "/cluster/show/" + cluster_id
    print url
    ret = requests.get(url,headers=headers)
    print ret.text

#maybe response is fail,but you can see image on your web interface
def image_create(instance_id):
    url = base_url + "/image/create"
    body = json.dumps({                        
        "instance-id": instance_id,
        "image-name": "edx_ucore",
    })
    ret = requests.post(url,headers=headers, data=body)
    print ret.text

def image_delete(image_id):
    url = base_url + "/image/delete/" + image_id
    ret = requests.delete(url,headers=headers)
    print ret.text

def image_list():
    url = base_url + "/image/list"
    ret = requests.get(url,headers=headers)
    print ret.text

def instance_list():
    url = base_url + "/instance/list"
    ret = requests.get(url,headers=headers)
    print ret.text

def init_parser():
    parser = argparse.ArgumentParser(description="test api argument")
    parser.add_argument('--image-id', action='store',
                        dest='image_id',
                        help='configure image id',
                        default='')
    parser.add_argument('--action', action='store',
                        dest='action',
                        help='configure action',
                        default='')
    parser.add_argument('--image-name', action='store',
                        dest='image_name',
                        help='configure image name',
                        default='')
    parser.add_argument('--config-id', action='store',
                        dest='config_id',
                        help='configure config id',
                        default='')
    parser.add_argument('--cluster-id', action='store',
                        dest='cluster_id',
                        help='configure cluster id',
                        default='')
    parser.add_argument('--instance-id', action='store',
                        dest='instance_id',
                        help='configure instance id',
                        default='')
    parser.add_argument('--ip', action='store',
                        dest='ip',
                        help='ext_ip',
                        default='')
    results = parser.parse_args()

    return results


parse_results = init_parser()
op = parse_results.action
if op == 'create-user':
    result = create_user()
    print result

elif op == 'get-webshell':
    result = get_webshell(parse_results.ip)
    print result

elif op == 'image-list':
    try:
        result = image_list()
    except Exception:
        raise Exception
    print result
elif op == 'image-show':
    try:
        result = image_show(parse_results.image_id)
    except Exception:
        raise Exception
    print result

elif op == 'image-delete':
    try:
        result = image_delete(parse_results.image_id)
    except Exception:
        raise Exception
    print result
elif op == 'image-create':
    image_name = parse_results.image_name
    instance_id = parse_results.instance_id
    try:
        result = image_create(instance_id)
    except Exception:
        raise Exception
    print result
elif op == 'cluster-config-list':
    try:
        result = cluster_config_list()
    except Exception:
        raise Exception
    print result
elif op == 'cluster-config-create':
    image_id = parse_results.image_id
    try:
        result = cluster_config_create(image_id)
    except Exception:
        raise Exception
    print result
elif op == 'cluster-config-show':
    config_id = parse_results.config_id
    try:
        result = cluster_config_show(config_id)
    except Exception:
        raise Exception
    print result
elif op == 'cluster-config-delete':
    config_id = parse_results.config_id
    try:
        result = cluster_config_delete(config_id)
    except Exception:
        raise Exception
    print result
elif op == 'cluster-list':
    try:
        result = cluster_list()
    except Exception:
        raise Exception
    print result
elif op == 'cluster-list-status':
    num_com = 0
    num_fail = 0
    try:
        result = cluster_list_status()
    except Exception:
        raise Exception
    for cluster in result:
	if cluster["status"] == "CREATE_COMPLETE":
	    num_com = num_com + 1
	if cluster["status"] == "DELETE_FAILED":
	    num_fail = num_fail + 1
        print cluster["status"]
    print num_com," CREATE_COMPLETE"
    print num_fail," DELETE_FAILED"
    print "complete"
elif op == 'cluster-show':
    cluster_id = parse_results.cluster_id
    try:
        result = cluster_show(cluster_id)
    except Exception:
        raise Exception
    print result
elif op == 'cluster-delete':
    cluster_id = parse_results.cluster_id
    try:
        result = cluster_delete(cluster_id)
    except Exception:
        raise Exception
    print result
elif op == 'cluster-delete-all':
    try:
	result = cluster_list_status()
	for cluster in result:
	    try:
	        ret = cluster_delete(cluster["id"])
	    except Exception:
        	raise Exception
    except Exception:
        raise Exception
    print "complete"
elif op == 'cluster-delete-failed':
    try:
	result = cluster_list_status()
	for cluster in result:
	    try:
		if cluster["status"] == "DELETE_FAILED":
	            ret = cluster_delete(cluster["id"])
	    except Exception:
        	raise Exception
    except Exception:
        raise Exception
    print "complete"
elif op == 'cluster-create':
    conf_id = parse_results.config_id
    try:
        result = cluster_create(conf_id)
    except Exception:
        raise Exception
    print result
elif op == 'instance-list':
    try:
        result = instance_list()
    except Exception:
        raise Exception
    print result
else:
    print "unknown operation!"
