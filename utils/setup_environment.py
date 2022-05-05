import os
from utils.load_file import full_load_yaml, full_load_csv

class SetupEnvironment:

    def __init__(self):
        self.device_list = ""
        self.command_list = ""
        self.change_number = ""
        self.test_type = ""


    def setup_pyats(self, device_filename, config_filename):
        self.device_list = full_load_csv(device_filename)
        self.command_list = full_load_yaml(config_filename)['pyats_learn_features']
        # print(os.getcwd())
        path = "/testbed"
        if not os.path.exists(path):
            print("#"*5 + f' create new direcotry {path} ' + "#"*5)
            os.makedirs(path)
        testbed_file = "../testbed/testbed.yaml"
        # self.command_list = full_load_yaml(config_filename)
        # self.change_number = input("Specify change numebr: ")
        print("#"*5 +  " create testbed.yaml " + "#"*5)
        os.system(f'pyats create testbed file --path {device_filename} --ouput {testbed_file}')
        
        return self


    def setup_netmiko(self, device_filename, config_filename):
        self.device_list = full_load_csv(device_filename)
        self.command_list = full_load_yaml(config_filename)
        self.change_number = input("Specify change numebr: ")
        # task_list = output[task].split()
        
        return self


        