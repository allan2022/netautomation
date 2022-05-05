import os
import json
import netmiko
from parse_all import parse_output
import threading
from datetime import datetime

class TestDevice:
    def __init__(self):
        self.all_devices = []
        self.all_command = []
        self.changenumber = ""
        self.testtype = ""
        self.change_folder = ""
        self.compare_folder = ""
        self.parse_folder = ""

    # log configuration for one device
    def run_command(self, a_device, all_commands, changenumber, compare_folder, parse_folder):
        netconnect = netmiko.ConnectHandler(**a_device)        
        for a_command in all_commands:

            # connect to device
            output = netconnect.send_command(a_command["command"])
            command_to_run = a_command["command"].replace(" ", "_")

            console_file = compare_folder + "/" + changenumber + "_" + a_device["host"] + "_" + command_to_run + "_" + "console.txt"
            with open(console_file, "w") as file:
                file.write(output + "\n")

            device_type = a_device["device_type"]
            parser_template = parse_folder + "/" + device_type + "_" + command_to_run + ".textfsm"

            ops_input = parse_output(console_file, parser_template) 
            ops_file = compare_folder + "/" + str(changenumber) + "_" + a_device["host"] + "_" + command_to_run + "_" + "ops.txt"            
            with open(ops_file, "w") as file:
                file.write(json.dumps(ops_input))

        # disconnect from device
        netconnect.disconnect()    


    # log configuration for all devices by calling run_command
    def connect_execute_output(self, all_devices, all_commands, changenumber, testtype):    
        current_dir = os.getcwd()
        output_folder = "Output"

        # create ouput folder for all validations
        if(not os.path.isdir(output_folder)):
            os.mkdir(output_folder)
 
        # create subfolder for specific change
        change_folder = os.path.join(output_folder, changenumber)  
        if(not os.path.isdir(change_folder)):
            os.mkdir(change_folder)

        # create subfolder for before & after for specific change
        compare_folder = changenumber + "_" + testtype + "_" + str(datetime.now()).replace(" ", "_")
        compare_folder = os.path.join(change_folder, compare_folder)
        if(not os.path.isdir(compare_folder)):
            os.mkdir(compare_folder)   
    
        self.change_folder = os.path.join(current_dir, change_folder)    
        self.compare_folder = os.path.join(current_dir, compare_folder)
        self.parse_folder = os.path.join(current_dir, 'parser')    

        # multi threads - one thread per device    
        for a_device in all_devices:
            t1 = threading.Thread(target=self.run_command, args=(a_device,all_commands, changenumber, self.compare_folder, self.parse_folder)) 
            t1.start()
            t1.join()
