import os
import json
import netmiko
from parsertools.parser_cli import parse_output
import threading
from datetime import datetime
from utils.new_folder import create_folder

class NetmikoCommand:
    def __init__(self):
        self.all_devices = []
        self.all_commands = []
        self.changenumber = ""
        self.testtype = ""
        self.change_folder = ""
        self.snapshot_folder = ""
        self.parse_folder = ""

    # log configuration for one device
    def exec_command(self, a_device, commands, changenumber, snapshot_folder, parse_folder):
        netconnect = netmiko.ConnectHandler(**a_device)        
        
        
        for a_command in commands:

            # connect to device
            output = netconnect.send_command(a_command)
            command_to_run = a_command.replace(" ", "_")

            console_file = snapshot_folder + "/" + changenumber + "_" + a_device["host"] + "_" + command_to_run + "_" + "console.txt"
            with open(console_file, "w") as file:
                file.write(output + "\n")

            device_type = a_device["device_type"]
            parser_template = parse_folder + "/" + device_type + "_" + command_to_run + ".textfsm"

            ops_input = parse_output(console_file, parser_template) 
            ops_file = snapshot_folder + "/" + str(changenumber) + "_" + a_device["host"] + "_" + command_to_run + "_" + "ops.txt"            
            with open(ops_file, "w") as file:
                file.write(json.dumps(ops_input))

        # disconnect from device
        netconnect.disconnect()    


    # log configuration for all devices by calling exec_command
    def snapshot (self, all_devices, all_commands, changenumber, testtype, output_folder):    
        # create subfolder for specific change
        change_folder = output_folder

        # create subfolder for each snapshot
        snapshot_folder = changenumber + "_" + testtype + "_" + str(datetime.now()).replace(" ", "_")
        snapshot_folder = os.path.join(change_folder, snapshot_folder)
        if(not os.path.isdir(snapshot_folder)):
            os.mkdir(snapshot_folder)   
    
        self.change_folder = os.path.join(current_dir, change_folder)    
        self.snapshot_folder = os.path.join(current_dir, snapshot_folder)
        self.parse_folder = os.path.join(current_dir, 'parsertemplate')    

        # multi threads - one thread per device    
        for a_device in all_devices:
            dev_type = a_device['device_type']
            commands = all_commands[dev_type]
            
            print("-"*20 + " commands for " + dev_type + "-"*20)
            for c in commands:
                print(c)
            print("\n")

            t1 = threading.Thread(target=self.exec_command, args=(a_device, commands, changenumber, self.snapshot_folder, self.parse_folder)) 
            t1.start()
            t1.join()
