import os
from utils.load_file import full_load_yaml, full_load_csv
from utils.new_folder import create_folder

class SetupEnvironment:

    def __init__(self):
        self.device_filename = ""
        self.device_list = ""
        self.command_list = ""
        self.change_number = ""
        self.test_type = ""
        try:
            self.change_number = input("Specify change numebr: ")
        except KeyboardInterrupt:
            print("\ntask aborted")



    def setup_pyats(self, dev_filename, env_filename):
        self.device_list = full_load_csv(dev_filename)
        self.command_list = full_load_yaml(env_filename)['pyats_learn_features']
        self.testbed_file = ""

        create_folder("testbed")

        self.testbed_file = f'testbed/testbed_{self.change_number}.yaml'
        if not os.path.exists(self.testbed_file):
            print("#"*5 +  f' create testbed_{self.change_number}.yaml ' + "#"*5)
            os.system(f'pyats create testbed file --path {dev_filename} --output {self.testbed_file}')

        return self


    def setup_netmiko(self, dev_filename, env_filename):
        self.device_filename = dev_filename
        self.device_list = self.command_list = full_load_csv(dev_filename)
        
        for dev, com in zip(self.device_list, self.command_list):
            
            print(type(dev))
            print(dev)
            print(type(com))
            print(com)

            dev['host'] = dev['hostname']
            dev.pop('hostname')
            dev.pop('protocol')
            dev.pop('platform')

            dev_type = dev['os']
            if dev_type == 'nxos':
                command_list = full_load_yaml(env_filename)['nxos_learn_commands']
                dev['device_type'] = "cisco_nxos"
                dev.pop('os')
            elif dev_type == 'iosxr':
                command_list = full_load_yaml(env_filename)['iosxe_learn_commands']
                dev['device_type'] = "cisco_xr"
                dev.pop('os')
            else:
                command_list = ""
                print(f'\n device type {dev_type} not supported. ')
            self.command_list.append(command_list)
            com['commands'] = command_list
        
        return self


        