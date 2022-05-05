import os
from utils.setup_environment import SetupEnvironment
from utils.new_folder import create_folder

# from pyatstools.pyatslearn import PyatsLearn
# from pyatstools.pyatsdiff import PyatsDiff

DEVICE_LIST_FILENAME = os.getcwd() + '/src/device_inventory.csv'
CORE_CONFIG_FILENAME = os.getcwd() + '/src/core_environment.yaml'

core_validation = SetupEnvironment()
core_validation.setup_pyats(DEVICE_LIST_FILENAME, CORE_CONFIG_FILENAME)
commands = core_validation.command_list
testbed = core_validation.testbed_file

create_folder("output")
# path = "testbed"
# if not os.path.exists(path):
#     print("#"*5 + f' create new direcotry {path} ' + "#"*5)
#     os.makedirs(path)

os.system(f'pyats learn {commands} --testbed-file {testbed} --output output')
