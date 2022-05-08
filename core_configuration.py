import os
from utils.get_task import get_task
from envtools.setup_environment import SetupEnvironment
from netmikotools.netmiko_command import NetmikoCommand

PYATS_DEVICE_LIST = os.getcwd() + '/src/pyats_validation_device_inventory.csv'
NETMIKO_DEVICE_LIST = os.getcwd() + '/src/netmiko_validation_device_inventory.csv'
CORE_ENVIRONMENT = os.getcwd() + '/src/core_environment.yaml'

class CoreConfiguration:
    def __init__(self):
        self.task_list = []
        self.task_select = ""

        try:
            self.task_list, self.task_select = get_task(CORE_ENVIRONMENT, 'sub_tasks')
        except KeyboardInterrupt:
            pass

    def core_validation_pyats(self):
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

    def core_validation_netmiko(self):
        netmiko_env = SetupEnvironment(CORE_ENVIRONMENT)
        if netmiko_env.change_number != "":
            netmiko_env.setup_validation_netmiko(NETMIKO_DEVICE_LIST, CORE_ENVIRONMENT, self.task_select)
            
            devices = netmiko_env.device_list
            commands = netmiko_env.command_list
            change_folder = netmiko_env.change_folder
            snapshot_folder = netmiko_env.snapshot_folder
            
            changenumber = netmiko_env.change_number
            parser = netmiko_env.parser_folder

            print("\n" + "-"*20 + " all devices to be validated " + "-"*20)
            for dev in devices:
                print('{} : {} '.format(dev['device_type'], dev['host'] ))
            print("-" * (40 + len(" all devices to be validated ")) +"\n")

            netmiko_dev = NetmikoCommand()
            netmiko_dev.snapshot(devices, commands, changenumber, snapshot_folder, parser)

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
    cv = CoreValidation()
    cv.core_validation_pyats()
    # cv.core_validation_netmiko()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n tast aborted")