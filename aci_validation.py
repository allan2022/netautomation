import os
from utils.get_task import get_task
from envtools.setup_environment import SetupEnvironment
from netmikotools.netmiko_command import NetmikoCommand

PYATS_DEVICE_LIST = os.getcwd() + '/src/pyats_validation_device_inventory.csv'
NETMIKO_DEVICE_LIST = os.getcwd() + '/src/netmiko_validation_device_inventory.csv'
CORE_ENVIRONMENT = os.getcwd() + '/src/core_environment.yaml'

class ACIValidation:
    def __init__(self):
        self.task_list = []
        self.task_select = ""

        try:
            self.task_list, self.task_select = get_task(CORE_ENVIRONMENT, 'sub_tasks')
        except KeyboardInterrupt:
            pass

        if self.task_select == None:
            print("\ntask not available")

    def aci_validation(self):
        
        if self.task_select != None:
            pyats_env = SetupEnvironment(CORE_ENVIRONMENT)

            if pyats_env.change_number != "":
                pyats_env.setup_validation_pyats(PYATS_DEVICE_LIST, CORE_ENVIRONMENT, self.task_select)

                devices = pyats_env.device_list
                commands = pyats_env.command_list
                testbed = pyats_env.testbed_file
                change_folder = pyats_env.change_folder
                snapshot_folder = pyats_env.snapshot_folder          

                os.system(f'pyats learn {commands} --testbed-file {testbed} --output {snapshot_folder}')

                if self.task_select == "postchange_snapshot_and_diff_prechange_snapshot":
                    print("#####################  compare postchange with prechange #########################")
                    before_folder = os.path.join(change_folder, 'prechange_snapshot_0')
                    os.system(f'pyats diff {before_folder} {snapshot_folder} --output {change_folder}/diff_dir')
                
                elif self.task_select == "postchange_snapshot_and_diff_last_postchange_snapshot":
                    print("#####################  compare postchange with last postchange #########################")
                    i = int(snapshot_folder.rsplit('_', 1)[-1]) - 1
                    before_folder = os.path.join(change_folder, ('postchange_snapshot_' + str(i)))
                    os.system(f'pyats diff {before_folder} {snapshot_folder} --output {change_folder}/diff_dir')
                
                else:
                    pass    

def main():
    av = ACIValidation()
    av.aci_validation()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n tast aborted")