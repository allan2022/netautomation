import os
from utils.get_task import get_task
from utils.diff_folder import diff_folder
from envtools.setup_environment import SetupEnvironment
from netmikotools.netmiko_command import NetmikoCommand

PYATS_DEVICE_LIST = os.getcwd() + '/src/pyats_validation_device_inventory.csv'
NETMIKO_DEVICE_LIST = os.getcwd() + '/src/netmiko_validation_device_inventory.csv'
CORE_ENVIRONMENT = os.getcwd() + '/src/core_environment.yaml'

class CoreValidation:
    def __init__(self):
        self.task_list = []
        self.task_select = ""

        try:
            self.task_list, self.task_select = get_task(CORE_ENVIRONMENT, 'sub_tasks')
        except KeyboardInterrupt:
            pass

        if self.task_select == None:
            print("\ntask not available")

    def core_validation_pyats(self):
        
        if self.task_select != None:
            pyats_env = SetupEnvironment(CORE_ENVIRONMENT)

            if pyats_env.change_number != "":
                pyats_env.setup_validation_pyats(PYATS_DEVICE_LIST, CORE_ENVIRONMENT, self.task_select)

                commands = pyats_env.command_list
                testbed = pyats_env.testbed_file
                change_folder = pyats_env.change_folder
                snapshot_folder = pyats_env.snapshot_folder          

                os.system(f'pyats learn {commands} --testbed-file {testbed} --output {snapshot_folder}')

                diff_folder(change_folder, snapshot_folder, self.task_select)

    def core_validation_netmiko(self):

        if self.task_select != None:
            netmiko_env = SetupEnvironment(CORE_ENVIRONMENT)

            if netmiko_env.change_number != "":
                netmiko_env.setup_validation_netmiko(NETMIKO_DEVICE_LIST, CORE_ENVIRONMENT, self.task_select)
                
                change_folder = netmiko_env.change_folder
                snapshot_folder = netmiko_env.snapshot_folder
                
                netmiko_dev = NetmikoCommand()
                netmiko_dev.snapshot_all(netmiko_env)                

                diff_folder(change_folder, snapshot_folder, self.task_select)

def main():
    cv = CoreValidation()
    # cv.core_validation_pyats()
    cv.core_validation_netmiko()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n test aborted")