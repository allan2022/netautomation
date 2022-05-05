import os
from utils.setup_environment import SetupEnvironment
from utils.new_folder import create_folder

# from pyatstools.pyatslearn import PyatsLearn
# from pyatstools.pyatsdiff import PyatsDiff

DEVICE_LIST = os.getcwd() + '/src/device_inventory.csv'
CORE_ENVIRONMENT = os.getcwd() + '/src/core_environment.yaml'

core_validation = SetupEnvironment()
core_validation.setup_pyats(DEVICE_LIST, CORE_ENVIRONMENT)
commands = core_validation.command_list
testbed = core_validation.testbed_file

a = create_folder("output")
output_folder = create_folder(f'output/{core_validation.change_number}')

os.system(f'pyats learn {commands} --testbed-file {testbed} --output {output_folder}')
