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
from utils.get_task import get_task
from core_validation import CoreValidation

NETWORK_VALIDATION = getcwd() + "/src/core_environment.yaml"

try:    
    task_list, task_select = get_task(NETWORK_VALIDATION, 'main_tasks')
except KeyboardInterrupt:
    pass

# def main():
#     match task_select:
#         case "core_validation":
#             print("core_validation")
#         case "aci_validation":
#             print("aci_validation")
#         case "juniper_validation":
#             print("juniper_validation")
#         case "f5_validation":
#             print("f5_validation")
#         case "fortinet_validation":
#             print("fortinet_validation") 
#         case "paloalto_validation":
#             print("paloalto_validation")                                               
#         case _:
#             print("\ntask not available")

def main():
    if task_select == "core_validation":
        task = CoreValidation()
        task.core_validation()
    elif task_select == "aci_validation":
        print("aci_validation")
    elif task_select == "juniper_validation":
        print("juniper_validation")
    elif task_select == "f5_validation":
        print("f5_validation")
    elif task_select == "fortinet_validation":
        print("fortinet_validation")
    elif task_select == "paloalto_validation":
        print("paloalto_validation")
    else:
        print("\ntask not available")

if __name__ == '__main__':
    try:
        main()
    except  (NameError, KeyboardInterrupt):
        print("\n task aborted")