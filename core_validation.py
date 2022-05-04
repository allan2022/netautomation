from os import getcwd
from utils.setup_environment import SetupEnvironment

# from pyatstools.pyatslearn import PyatsLearn
# from pyatstools.pyatsdiff import PyatsDiff

DEVICE_LIST_FILENAME = getcwd() + '/src/device_inventory.csv'
CORE_CONFIG_FILENAME = getcwd() + '/src/core_envrionment.yaml'

core_validation = SetupEnvironment()
core_validation.setup_pyats(DEVICE_LIST_FILENAME, CORE_CONFIG_FILENAME)