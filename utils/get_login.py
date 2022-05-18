from utils.load_file import full_load_yaml
from getpass import getpass

def get_login(yaml_filename, env=None):
    hostname = None
    username = None
    password = None

    output = full_load_yaml(yaml_filename)
    
    if output != None:
        try:
            hostname = full_load_yaml(yaml_filename)['aci_networks'][env]['hostname']
            username = full_load_yaml(yaml_filename)['aci_networks'][env]['username']
            password = full_load_yaml(yaml_filename)['aci_networks'][env]['password']
        except (IndexError, ValueError, KeyboardInterrupt):
            print("please enter correct aci login info in core_environement.yaml file")

    if hostname == "input hostname":
        hostname = input("Enter APIC Hostname/IP: ")

    if username == "input username":
        username = input("Enter APIC Username: ")
        
    if password == "input password":
        password = getpass("Enter APIC Password: ")        

    return hostname, username, password



    