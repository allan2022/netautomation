from utils.load_yaml import full_load

class SetupEnvironment:

    def __init__(self, device_filename, command_filename):
        self.device_list = full_load(device_filename)
        self.command_list = full_load(command_filename)
        self.change_number = ""
        self.test_type = ""


    def setup_pyats(self):
        self.device_list = "device_inventory.csv"
        self.command_lsit = "command_inventory.csv"
        self.change_number = input("Specify change numebr: ")


    def setup_netmiko(self):
        self.device_list = "device_inventory.csv"
        self.command_lsit = "command_inventory.csv"
        self.change_number = input("Specify change numebr: ")




