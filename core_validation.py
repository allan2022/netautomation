from os import getcwd()
from utils.setup_environment import TestEnv

from utils.get_task import get_task

from pyatstools.pyatslearn import PyatsLearn
from pyatstools.pyatsdiff import PyatsDiff



ENVIRONMENT_CONFIG = getcwd() + '/src/core_envrionment.yaml'
DEVICE_LIST = getcwd() + '/src/device_inventory.csv'