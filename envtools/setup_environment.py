import os
from utils.load_file import full_load_yaml, full_load_csv, load_command_csv
from utils.new_folder import create_folder
from utils.get_login import get_login
from utils.check_folder import check_folder

class SetupEnvironment:

    def __init__(self, env_filename):
        self.device_list = ""
        self.command_list = ""
        self.change_number = ""
        self.change_folder = ""
        self.snapshot_folder = ""
        self.parser_folder = ""
        self.testbed_file = ""

        try:
            self.change_number = input("\nSpecify change numebr: ")
        except KeyboardInterrupt:
            print("\ntask aborted")

        output_folder = full_load_yaml(env_filename)['output_directory']
        if self.change_number != "":
            self.change_folder = os.path.join(os.getcwd(), output_folder, self.change_number)
            self.change_folder = create_folder(self.change_folder)

    def setup_validation_pyats(self, dev_filename, env_filename, test_type):
        self.device_list = full_load_csv(dev_filename)
        self.command_list = full_load_yaml(env_filename)['pyats_learn_features']

        testbed_folder = full_load_yaml(env_filename)['testbed_directory']
        create_folder(testbed_folder)

        self.testbed_file = os.path.join(os.getcwd(), f'{testbed_folder}/{testbed_folder}_{self.change_number}.yaml')

        if not os.path.exists(self.testbed_file):
            os.system(f'pyats create testbed file --path {dev_filename} --output {self.testbed_file}')

        self.snapshot_folder = check_folder(self.change_folder, test_type)

        return self

    def setup_validation_netmiko(self, dev_filename, env_filename, test_type):  
        self.device_list = full_load_csv(dev_filename)
        self.command_list = {}   
        
        parsertemplate = full_load_yaml(env_filename)['parsertemplate_direcotry']
        self.parser_folder = os.path.join(os.getcwd(), parsertemplate)     

        for dev in self.device_list:
            dev_type = dev['device_type']
            if dev_type == "cisco_nxos":
                command_list = full_load_yaml(env_filename)['nxos_learn_commands']
                self.command_list['cisco_nxos'] = command_list
            elif dev_type == "cisco_xr":
                command_list = full_load_yaml(env_filename)['iosxe_learn_commands']
                self.command_list['cisco_xr'] = command_list
            elif dev_type == "f5_tmsh":
                command_list = full_load_yaml(env_filename)['f5_tmsh_learn_commands']
                self.command_list['f5_tmsh'] = command_list
            elif dev_type == "fortinet":
                command_list = full_load_yaml(env_filename)['fortinet_learn_commands']
                self.command_list['fortinet'] = command_list 
            else:
                command_list = ""
                print(f'\n device type {dev_type} not supported. ')

        self.snapshot_folder = check_folder(self.change_folder, test_type)

        return self

    def setup_configuration_netmiko(self, dev_filename, env_filename, config_type):  
        self.device_list = full_load_csv(dev_filename)
        self.command_list = []

        if (config_type == "config_from_command"):
            try:
                command = input("\ntype tmsh command: ")
            except KeyboardInterrupt:
                print("\ntask aborted")
            self.command_list.append(command)

        elif (config_type == "config_from_file"):
            config_file = full_load_yaml(env_filename)['config_file']
            config_file = os.path.join(os.getcwd(), config_file)
            self.command_list = load_command_csv(config_file) 

        else:
            pass

        return self

    def setup_validation_aci(self, env_filename, test_type, aci_env):  
        hostname, username, password = get_login(env_filename, aci_env)
        self.snapshot_folder = check_folder(self.change_folder, test_type)

        self.base_url = 'https://{apic_host}/api/'.format(apic_host=hostname)
        auth_bit = "aaaLogin.json"
        self.auth_url = self.base_url + auth_bit

        # JSON auth data for POST
        self.auth_data = {
            "aaaUser":{
                "attributes":{
                "name":username,
                "pwd":password
                }
            }
        }

        return self
        