from os import getcwd
from utils.get_task import get_task
from core_validation import CoreValidation
from f5_validation import F5Validation
from fortinet_validation import FortinetValidation
from aci_validation import ACIValidation

CORE_ENVIRONMENT = getcwd() + "/src/core_environment.yaml"

try:    
    task_list, task_select = get_task(CORE_ENVIRONMENT, 'main_tasks')
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
    if task_select == "core_validation_pyats":
        task = CoreValidation()
        task.core_validation_pyats()
    elif task_select == "core_validation_netmiko":
        task = CoreValidation()
        task.core_validation_netmiko()
    elif task_select == "aci_validation":
        task = ACIValidation()
        task.aci_validation()
    elif task_select == "juniper_validation":
        print("juniper_validation")
    elif task_select == "f5_validation":
        task = F5Validation()
        task.f5_validation_netmiko()
    elif task_select == "fortinet_validation":
        task = FortinetValidation()
        task.fortinet_validation_netmiko()
    elif task_select == "paloalto_validation":
        print("paloalto_validation")
    else:
        print("\ntask not available")

if __name__ == '__main__':
    try:
        main()
    except  (NameError, KeyboardInterrupt):
        print("\n task aborted")