import json
import netmiko
import threading
from parsertools.parser_cli import parse_output

class NetmikoCommand:
    def __init__(self):
        pass

    # log configuration for one device
    def exec_snapshot(self, device, commands, changenumber, snapshot_folder, parser_folder):
        netconnect = netmiko.ConnectHandler(**device)

        for command in commands:
            device_type = device["device_type"]          

            # if device_type == "fortinet":
            #     output = netconnect.send_config_set(command['cmd'])
            #     command_name = "get_system_session_list"
            # else:
            #     output = netconnect.send_command(command)
            #     command_name = command.replace(" ", "_")

            if device_type == "fortinet":
                netconnect.send_command("config vdom")
                netconnect.send_command("edit root")

            output = netconnect.send_command(command)
            command_name = command.replace(" ", "_")


            console_file = snapshot_folder + "/" + changenumber + "_" + device["host"] + "_" + command_name + "_" + "console.txt"
            with open(console_file, "w") as file:
                file.write(output + "\n")

            parser_template = parser_folder + "/" + device_type + "_" + command_name + ".textfsm"

            ops_input = parse_output(console_file, parser_template) 
            ops_file = snapshot_folder + "/" + str(changenumber) + "_" + device["host"] + "_" + command_name + "_" + "ops.txt"            
            with open(ops_file, "w") as file:
                file.write(json.dumps(ops_input))

        netconnect.disconnect()    

    # log configuration for all devices by calling exec_snapshot
    def snapshot (self, devices, all_commands, changenumber, snapshot_folder, parser_folder):    
    
        # multi threads - one thread per device    
        for device in devices:
            dev_type = device['device_type']
            commands = all_commands[dev_type]
            
            print("-"*20 + " commands for " + dev_type + " " + "-"*20)
            for command in commands:
                print(command)
            print("\n")

            t1 = threading.Thread(target=self.exec_snapshot, args=(device, commands, changenumber, snapshot_folder, parser_folder)) 
            t1.start()
            t1.join()

    def exec_f5_config(self, device, commands):
        netconnect = netmiko.ConnectHandler(**device)
        devname = device['host']

        print("-"*20 + f' commands for {devname} ' + "-"*20)
        for command in commands:
            expect_prompt = r"(root@.*#|\s*|[#|\$]\s*$)"
            output = netconnect.send_command_expect(command, expect_string=expect_prompt, cmd_verify=False)

            if output == "":
                print(f'{command} \n -- succeed\n')
            else:
                print(f'{command} \n -- failed\n')

        netconnect.disconnect()   

    # config for all devices by calling exec_command
    def config (self, devices, commands):    

        # multi threads - one thread per device    
        for device in devices:        
            t1 = threading.Thread(target=self.exec_f5_config, args=(device, commands)) 
            t1.start()
            t1.join()

    def fortinet_vdom(self, device, commands):
        netconnect = netmiko.ConnectHandler(**device)
        devname = device['host']

        print("-"*20 + f' commands for {devname} ' + "-"*20)
        for command in commands:
            expect_prompt = r"(root@.*#|\s*|[#|\$]\s*$)"
            output = netconnect.send_command_expect(command, expect_string=expect_prompt, cmd_verify=False)

            if output == "":
                print(f'{command} \n -- succeed\n')
            else:
                print(f'{command} \n -- failed\n')

        netconnect.disconnect()   
