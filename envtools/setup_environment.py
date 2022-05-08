import os
from utils.load_file import full_load_yaml, full_load_csv
from utils.new_folder import create_folder

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

        if test_type.startswith('prechange_snapshot'):
            for i in range(20):
                self.snapshot_folder = os.path.join(self.change_folder, ('prechange_snapshot_' + str(i)))
                if not os.path.exists(self.snapshot_folder):
                    create_folder(self.snapshot_folder)
                    break
        elif test_type.startswith('postchange_snapshot'):
            for i in range(20):
                self.snapshot_folder = os.path.join(self.change_folder, ('postchange_snapshot_' + str(i)))
                if not os.path.exists(self.snapshot_folder):
                    create_folder(self.snapshot_folder)
                    break
        else:
            print("test type not supported")

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
            else:
                command_list = ""
                print(f'\n device type {dev_type} not supported. ')

        if test_type.startswith('prechange_snapshot'):
            for i in range(20):
                self.snapshot_folder = os.path.join(self.change_folder, ('prechange_snapshot_' + str(i)))
                if not os.path.exists(self.snapshot_folder):
                    create_folder(self.snapshot_folder)
                    break
        elif test_type.startswith('postchange_snapshot'):
            for i in range(20):
                self.snapshot_folder = os.path.join(self.change_folder, ('postchange_snapshot_' + str(i)))
                if not os.path.exists(self.snapshot_folder):
                    create_folder(self.snapshot_folder)
                    break
        else:
            print("test type not supported")

        return self

    def setup_configuration_netmiko(self, dev_filename, env_filename, test_type):  
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
            else:
                command_list = ""
                print(f'\n device type {dev_type} not supported. ')

        if test_type.startswith('prechange_snapshot'):
            for i in range(20):
                self.snapshot_folder = os.path.join(self.change_folder, ('prechange_snapshot_' + str(i)))
                if not os.path.exists(self.snapshot_folder):
                    create_folder(self.snapshot_folder)
                    break
        elif test_type.startswith('postchange_snapshot'):
            for i in range(20):
                self.snapshot_folder = os.path.join(self.change_folder, ('postchange_snapshot_' + str(i)))
                if not os.path.exists(self.snapshot_folder):
                    create_folder(self.snapshot_folder)
                    break
        else:
            print("test type not supported")

        return self

        