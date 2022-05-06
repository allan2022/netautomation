import os
from utils.get_task import get_task
from validationtools.setup_environment import SetupEnvironment
from netmikotools.netmiko_command import NetmikoCommand

# from pyatstools.pyatslearn import PyatsLearn
# from pyatstools.pyatsdiff import PyatsDiff

DEVICE_LIST = os.getcwd() + '/src/device_inventory.csv'
CORE_ENVIRONMENT = os.getcwd() + '/src/core_environment.yaml'


class CoreValidation:
    def __init__(self):
        self.devices = ""
        self.commands = ""
        self.testbed = ""
        self.change_folder = ""
        self.task_list = []
        self.task_select = ""

        try:
            self.task_list, self.task_select = get_task(CORE_ENVIRONMENT, 'sub_tasks')
        except KeyboardInterrupt:
            pass

    def core_validation_pyats(self):
        core_validation = SetupEnvironment()
        if core_validation.change_number != "":
            core_validation.setup_pyats(DEVICE_LIST, CORE_ENVIRONMENT, self.task_select)

            self.devices = core_validation.device_list
            self.commands = core_validation.command_list
            self.testbed = core_validation.testbed_file
            self.change_folder = core_validation.change_folder
            self.snapshot_folder = core_validation.snapshot_folder

            os.system(f'pyats learn {self.commands} --testbed-file {self.testbed} --output {self.snapshot_folder}')

            if self.task_select == "postchange_snapshot_and_diff_prechange_snapshot":
                print("#####################  compare postchange with prechange #########################")
                before_folder = os.path.join(self.change_folder, 'prechange_snapshot_0')
                os.system(f'pyats diff {before_folder} {self.snapshot_folder} --output {self.change_folder}/diff_dir')
            elif self.task_select == "postchange_snapshot_and_diff_last_postchange_snapshot":
                print("#####################  compare postchange with last postchange #########################")
                i = int(self.snapshot_folder.rsplit('_', 1)[-1]) - 1
                before_folder = os.path.join(self.change_folder, ('postchange_snapshot_' + str(i)))
                os.system(f'pyats diff {before_folder} {self.snapshot_folder} --output {self.change_folder}/diff_dir')
            else:
                print("task not supported")    

    def core_validation_netmiko(self):
        core_validation = SetupEnvironment()
        if core_validation.change_number != "":
            core_validation.setup_netmiko(DEVICE_LIST, CORE_ENVIRONMENT, self.task_select)
            
            self.devices = core_validation.device_list
            self.commands = core_validation.command_list
            self.change_folder = core_validation.change_folder
            self.snapshot_folder = core_validation.snapshot_folder

            print("\n" + "-"*20 + " all devices to be validated " + "-"*20)
            for dev in self.devices:
                print('{} : {} '.format(dev['device_type'], dev['host'] ))
            print("-" * (40 + len(" all devices to be validated ")) +"\n")

            dev = NetmikoCommand()
            dev.snapshot(self.devices, self.commands, core_validation.change_number, self.task_select, self.change_folder)

            if self.task_select == "postchange_snapshot_and_diff_prechange_snapshot":
                print("#####################  compare postchange with prechange #########################")
                before_folder = os.path.join(self.change_folder, 'prechange_snapshot_0')
                os.system(f'pyats diff {before_folder} {self.snapshot_folder} --output {self.change_folder}/diff_dir')
            elif self.task_select == "postchange_snapshot_and_diff_last_postchange_snapshot":
                print("compare postchange with last poastchange")

def main():
    cv = CoreValidation()
    cv.core_validation_pyats()
    cv.core_validation_netmiko()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n tast aborted")