from os import getcwd
from utils.setup_environment import SetupEnvironment

# from pyatstools.pyatslearn import PyatsLearn
# from pyatstools.pyatsdiff import PyatsDiff

CORE_ENV_FILENAME = getcwd() + '/src/core_envrionment.yaml'
DEVICE_LIST_FILENAME = getcwd() + '/src/device_inventory.csv'

core_validation = SetupEnvironment()