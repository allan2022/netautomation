import os
from utils.setup_environment import SetupEnvironment
from utils.new_folder import create_folder

# from pyatstools.pyatslearn import PyatsLearn
# from pyatstools.pyatsdiff import PyatsDiff

DEVICE_LIST = os.getcwd() + '/src/device_inventory.csv'
CORE_ENVIRONMENT = os.getcwd() + '/src/core_environment.yaml'


class CoreValidation:
    def __init__(self):
        self.commands = ""
        self.testbed = ""
    
    def core_validation(self):
        core_validation = SetupEnvironment()
        if core_validation.change_number != "":
            core_validation.setup_pyats(DEVICE_LIST, CORE_ENVIRONMENT)

            self.commands = core_validation.command_list
            self.testbed = core_validation.testbed_file

            a = create_folder("output")
            output_folder = create_folder(f'output/{core_validation.change_number}')

            os.system(f'pyats learn {self.commands} --testbed-file {self.testbed} --output {output_folder}')

def main():
    cv = CoreValidation()
    cv.core_validation()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n tast aborted")