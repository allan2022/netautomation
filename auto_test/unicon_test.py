from unicon import Connection
import time
from jinja2 import Environment, FileSystemLoader
import yaml

#this prepares the config
accesslists = yaml.load(open('acl.yaml'), Loader=yaml.SafeLoader)
env = Environment(loader = FileSystemLoader('.'), trim_blocks=True, autoescape=True)
template = env.get_template('acl.j2')
acl_config = template.render(data=accesslists)
command = acl_config.split("\n")

#this prepares the connection
c = Connection(hostname='R1', start=['ssh 192.168.126.140'], os='ios', credentials={'default': {'username': 'cisco', 'password': 'cisco'}, 'secret': 'cisco'},)
c.connect()

# command = []
# for item in preoutput:
#     command.append(item)

#this actually configures the router
print(command)
output = c.configure(command)