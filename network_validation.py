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

def main(task_select):
    match task_select:
        case "aci":
            print("aci")
        case "core":
            print("core")
        case _:
            print("not available")

if __name__ == '__main__':
    main(task_list)

