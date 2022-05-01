from unicon import Connection
import time
from jinja2 import Environment, FileSystemLoader
import yaml

#this prepares the config
accesslists = yaml.load(open('acl.yaml'), Loader=yaml.SafeLoader)
env = Environment(loader = FileSystemLoader('.'), trim_blocks=True, autoescape=True)
template = env.get_template('acl.j2')
acl2_config = template.render(data=accesslists)
preoutput = acl2_config.split("\n")
# print(preoutput)

#this prepares the connection
c = Connection(hostname='R1', start=['ssh 192.168.126.140'], os='ios', credentials={'default': {'username': 'cisco', 'password': 'cisco'}, 'secret': 'cisco'},)
c.connect()

#This checks how many commands the config set has. This is because unicon's configure method adds ''end'' after each command. So in case of nested commands we need to push the whole set of commands (e.g. interface loop0,ip addr 1.1.1.1 255.255.255.255). So command is a list, to which I push all elements of the config, then the whole list is pushed to the router.

# x = len(preoutput)
# y=0
# command = []
# while y<x:
#   command.append(preoutput[x-x+y])
#   y = y+1

print(type(acl2_config))
print(type(preoutput))
command = []
for item in preoutput:
    command.append(item)

#this actually configures the router
print(command)
output = c.configure(command)