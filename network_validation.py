"""
1. Read task
2. Setup environment
3. Network validation
    - ACI validation
    - Cisco validation
    - Juniper validation
    - Fortinet validation
    - Palo Alto validation
    - F5 validation
    - IPAM validation
    - Splunk validation
"""
from os import getcwd
import yaml
from utils.get_task import get_task

NETWORK_VALIDATION = getcwd() + "/src/all_validation.yaml"

task_list, task_select = get_task(NETWORK_VALIDATION)

print(type(task_select))

def main():
    match task_select:
        case "core_validation":
            print("core_validation")
        case "aci_validation":
            print("core_validation")
        case "juniper_validation":
            print("juniper_validation")
        case "f5_validation":
            print("f5_validation")
        case "fortinet_validation":
            print("fortinet_validation") 
        case "paloalto_validation":
            print("paloalto_validation")                                               
        case _:
            print("not available")

if __name__ == '__main__':
    main()
