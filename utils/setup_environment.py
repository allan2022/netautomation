from utils.load_file import full_load_yaml, full_load_csv

class SetupEnvironment:

    def __init__(self):
        self.device_list = ""
        self.command_list = ""
        self.change_number = ""
        self.test_type = ""


    def setup_pyats(self, device_filename, config_filename):
        self.device_list = full_load_csv(device_filename)
        self.command_list = full_load_yaml(config_filename)
        self.change_number = input("Specify change numebr: ")


    def setup_netmiko(self, device_filename, config_filename):
        self.device_list = full_load_csv(device_filename)
        self.command_list = full_load_yaml(config_filename)
        self.change_number = input("Specify change numebr: ")




