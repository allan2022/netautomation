import sys
"""
addd ACL to cisco router from acl.j2 with render from acl.yaml

ip access-list extended permit_www
permit ip 192.168.122.100 0.0.0.0 8.8.8.8 0.0.0.0
"""


from netmiko import ConnectHandler
import time
from netmiko import redispatch
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader
import yaml

def connect(hostip):
    net_connect = ConnectHandler(device_type='cisco_ios', host=hostip, username='cisco', password='cisco', secret='cisco')
    net_connect.find_prompt()
    net_connect.enable()
    accesslists = yaml.load(open('acl.yaml'), Loader=yaml.SafeLoader)
    env = Environment(loader = FileSystemLoader('.'))
    template = env.get_template('acl.j2') 
    acl_config = template.render(data=accesslists) 
    print(acl_config) 
    print(f"Logged into {hostip} successfully") 
    output = net_connect.send_config_set(acl_config.split("\n"))

if __name__ == "__main__": 
    ip = sys.argv[1] 
    connect(ip)