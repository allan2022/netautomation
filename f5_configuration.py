import os
from utils.get_task import get_task
from envtools.setup_environment import SetupEnvironment
from netmikotools.netmiko_command import NetmikoCommand

F5_DEVICE_LIST = os.getcwd() + '/src/f5_configuration_device_inventory.csv'
F5_ENVIRONMENT = os.getcwd() + '/src/configuration_environment.yaml'

class F5Configuration:
    def __init__(self):
        self.task_list = []
        self.task_select = ""

        try:
            self.task_list, self.task_select = get_task(F5_ENVIRONMENT, 'config_tasks')
        except KeyboardInterrupt:
            pass

    def f5_config(self):
        f5_env = SetupEnvironment(F5_ENVIRONMENT)
        if f5_env.change_number != "":
            f5_env.setup_configuration_netmiko(F5_DEVICE_LIST, F5_ENVIRONMENT, self.task_select)
            
            devices = f5_env.device_list
            commands = f5_env.command_list
            change_folder = f5_env.change_folder
            snapshot_folder = f5_env.snapshot_folder
            
            changenumber = f5_env.change_number
            parser = f5_env.parser_folder

            print("\n" + "-"*20 + " all devices to be configured " + "-"*20)
            for dev in devices:
                print('{} : {} '.format(dev['device_type'], dev['host'] ))
            print("-" * (40 + len(" all devices to be configured ")) +"\n")

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
    cv = F5Configuration()
    cv.f5_config()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n tast aborted")