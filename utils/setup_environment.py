import os
from utils.load_file import full_load_yaml, full_load_csv

class SetupEnvironment:

    def __init__(self):
        self.device_list = ""
        self.command_list = ""
        self.change_number = input("Specify change numebr: ")
        self.test_type = ""


    def setup_pyats(self, device_filename, config_filename):
        self.device_list = full_load_csv(device_filename)
        self.command_list = full_load_yaml(config_filename)['pyats_learn_features']
        self.testbed_file = ""

        path = "testbed"
        if not os.path.exists(path):
            print("#"*5 + f' create new direcotry {path} ' + "#"*5)
            os.makedirs(path)

        self.testbed_file = f'testbed/testbed_{self.change_number}.yaml'
        if not os.path.exists(self.testbed_file):
            print("#"*5 +  f' create testbed_{self.change_number}.yaml ' + "#"*5)
            os.system(f'pyats create testbed file --path {device_filename} --output {self.testbed_file}')

        return self


    def setup_netmiko(self, device_filename, config_filename):
        self.device_list = full_load_csv(device_filename)
        self.command_list = full_load_yaml(config_filename)['iosxe_self_learn_commands']
        # task_list = output[task].split()
        
        return self


        