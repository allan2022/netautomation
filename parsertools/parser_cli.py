import json
import textfsm

def parse_output(console_file, parser_template):
    result_dict = {}
    with open(console_file, "r") as console_output, open(parser_template, "r") as template :  
            fsm = textfsm.TextFSM(template)
            result_list = fsm.ParseTextToDicts(console_output.read())
            for item in result_list:
                first_key = list(item.keys())[0]
                first_value = list(item.values())[0]
                if (first_key == "VRF"):
                     second_key = list(item.keys())[2]   
                     second_value = list(item.values())[2]   
                     result_dict.update({first_key + ": " + first_value + ", " + second_key + ": " + second_value: item})
                else:        
                     result_dict.update({first_value: item})        
    return result_dict

