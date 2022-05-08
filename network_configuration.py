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
from core_configuration import CoreConfiguration
from f5_configuration import F5Configuration

CONFIG_ENVIRONMENT = getcwd() + "/src/configuration_environment.yaml"

try:    
    task_list, task_select = get_task(CONFIG_ENVIRONMENT, 'main_tasks')
except KeyboardInterrupt:
    pass

def main():
    if task_select == "core_configuraiton":
        print("core_configuration")
    elif task_select == "f5_configuration":
        print("f5_configuraiton")
    else:
        print("\ntask not available")

if __name__ == '__main__':
    try:
        main()
    except  (NameError, KeyboardInterrupt):
        print("\n task aborted")