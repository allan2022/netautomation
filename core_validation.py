import os
from validationtools.setup_environment import SetupEnvironment
from utils.new_folder import create_folder
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
        self.type = ""
    
    def core_validation_pyats(self):
        core_validation = SetupEnvironment()
        if core_validation.change_number != "":
            core_validation.setup_pyats(DEVICE_LIST, CORE_ENVIRONMENT)

            self.devices = core_validation.device_list
            self.commands = core_validation.command_list
            self.testbed = core_validation.testbed_file

            a = create_folder("output")
            output_folder = create_folder(f'output/{core_validation.change_number}')

            os.system(f'pyats learn {self.commands} --testbed-file {self.testbed} --output {output_folder}')

    def core_validation_netmiko(self):
        core_validation = SetupEnvironment()
        if core_validation.change_number != "":
            core_validation.setup_netmiko(DEVICE_LIST, CORE_ENVIRONMENT)
            
            self.devices = core_validation.device_filename
            self.commands = core_validation.command_list
            self.type = 'prechange'

            a = create_folder("output")
            output_folder = create_folder(f'output/{core_validation.change_number}')

            print(self.devices)
            print("######################################################################")
            print(self.commands)
            print("###################### run netmiko commands ##########################")

            dev = NetmikoCommand()
            dev.connect_execute_output(self.devices, self.commands, core_validation.change_number, self.type)


def main():
    cv = CoreValidation()
    cv.core_validation_pyats()
    cv.core_validation_netmiko()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n tast aborted")