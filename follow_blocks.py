#!/usr/bin/env python
# Licence is BSD
# Author is gled-rs on github.
# Goal of this script is to replicate domain blocks from a group of trusted instances.
DEFAULT_SEVERITY='noop'
DEFAULT_REJECT_MEDIA=False
DEFAULT_REJECT_REPORTS=False
DEFAULT_OBFUSCATE=False

import os
import json
import requests
import validators

def get_instance_software(instance):
    r = requests.get('https://'+instance+'/nodeinfo/2.0')
    if r.status_code != 200:
        print("Error with requesting %s instance info, status code %d" % (instance,r.status_code))
    return r.json()['software']['name']

def get_blocked_list(instance,auth=''):
    instance_type = get_instance_software(instance)
    if instance_type == 'gotosocial' or auth != '':
        path='/api/v1/admin/domain_blocks'
    elif instance_type == 'mastodon':
        path='/api/v1/instance/domain_blocks'
    else:
        print('Unsupported instance type '+instance_type)
        return json.loads('{}')
    if auth != '':
        headers = {'Authorization':'Bearer '+auth}
    else:
        headers = {}
    r = requests.get('https://'+instance+path,headers=headers)
    if r.status_code != 200:
        print("Error with requesting %s block list, status code %d" % (instance,r.status_code))
        return json.loads('{}')
    return r.json()

def post_block_list(blocklist):
    headers = {'Authorization':'Bearer '+config['API_KEY']}
    path='/api/v1/admin/domain_blocks'
    for d in blocklist:
        print("Blocking %s with severity %s because %s" % (d['domain'],d['severity'],d['public_comment']))
        #requests.post('https://'+config['MY_INSTANCE']+path,headers=headers,data=d)


config_file = os.path.dirname(os.path.realpath(__file__))+'/config.json'
if not os.path.isfile(config_file):
    print('No config file found, let\'s generate one')
    config={}
    config['MY_INSTANCE']=input('What is your instance domain name ? ( example: my.social.domain )\n')
    config['API_KEY']=input('What is your admin account API key ( to add blocked domains to your instance, see readme for an idea on how to get one )\n')
    ti=input('Now please give us a list of instance you trust to automatically add their block decisions to your instance, comma separated and no spaces ( example: instance1.domain,instance2.domain )\n')
    config['TRUSTED_INSTANCES'] = ti.split(',')
    dni=input('Now please give us a list of instance you will not block automatically, comma separated, no spaces ( example: donotblock.domain,donotblock2.domain)\n')
    config['EXEMPT_INSTANCES'] = dni.split(',')
    with open(config_file,'w') as f:
        json.dump(config,f)

with open(config_file,'r') as f:
    config=json.load(f)

if config['API_KEY'] == '':
    raise Exception('API_KEY empty, please edit config.json')
if config['MY_INSTANCE'] == '':
    raise Exception('MY_INSTANCE empty, please edit config.json')
if len(config['TRUSTED_INSTANCES']) == 0:
    raise Exception('TRUSTED_INSTANCES list empty, please edit config.json')

# Get my list of blocked instances
my_blocked=[]
my_blocklist=get_blocked_list(config['MY_INSTANCE'],config['API_KEY'])
for i in my_blocklist:
    my_blocked.append(i['domain'])

to_block=[]
for instance in config['TRUSTED_INSTANCES']:
    their_blocks = get_blocked_list(instance)
    for i in their_blocks:
        if validators.url('http://'+i['domain']):
            if not i['domain'] in my_blocked and not i['domain'] in to_block and not i['domain'] in config['EXEMPT_INSTANCES']:
                d={'domain':i['domain']}
                if 'severity' in i:
                    d['severity'] = i['severity']
                else:
                    d['severity'] = DEFAULT_SEVERITY
                if 'comment' in i and not i['comment'] is None:
                    d['public_comment'] = 'From '+instance+' '+i['comment']
                else:
                    d['public_comment'] = 'From '+instance
                if 'reject_media' in i:
                    d['reject_media'] = i['reject_media']
                else:
                    d['reject_media'] = DEFAULT_REJECT_MEDIA
                if 'reject_reports' in i:
                    d['reject_reports'] = i['reject_reports']
                else:
                    d['reject_reports'] = DEFAULT_REJECT_REPORTS
                d['obfuscate'] = DEFAULT_OBFUSCATE
                to_block.append(d)

post_block_list(to_block)
