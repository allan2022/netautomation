"""
1. Read task
2. Setup environment
3. Network configuration
    - ACI configuration
    - Cisco configuration
    - Juniper configuration
    - Fortinet configuration
    - Palo Alto configuration
    - F5 configuration
    - IPAM configuration
    - Splunk configuration
"""
from os import getcwd
from utils.get_task import get_task

NETWORK_CONFIG = getcwd() + "/src/all_configuration.yaml"

task_list, task_select = get_task(NETWORK_CONFIG)

def main():
    match task_select:
        case "core_configuration":
            print("core_configuration")
        case "aci_configuration":
            print("aci_configuration")
        case "juniper_configuration":
            print("juniper_configuration")
        case "f5_configuration":
            print("f5_configuration")
        case "fortinet_configuration":
            print("fortinet_configuration") 
        case "paloalto_configuration":
            print("paloalto_configuration")                                               
        case _:
            print("\ntask not available")

if __name__ == '__main__':
    main()
