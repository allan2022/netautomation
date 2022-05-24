import json
from xml.etree.ElementTree import QName
from parsertools.parser_cli import parse_output

def save_output (command, output, c_num, s_folder, p_folder, host, d_type):
    c_name = command.replace(" ", "_")
    prefix = s_folder + "/" + c_num + "_" + host + "_" + c_name

    con_file = prefix + "_console.text"
    with open(con_file, 'w') as file:
        file.write(output + "\n")

    p_template = p_folder + "/" + d_type + "_" + c_name + ".textfsm"
    ops_input = parse_output(con_file, p_template)

    ops_file = prefix + "_ops.txt"
    with open(ops_file, 'w') as file:
        file.write(json.dumps(ops_input))

