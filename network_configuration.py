
"""
1. Read task
2. Network validation
3. Implement change
    - ACI change
    - Cisco change
    - Juniper change
    - Fortinet change
    - Palo Alto change
    - F5 change
    - IPAM change
4. Network validation

"""
import yaml

yaml_file_name = "src/all_validation.yaml"
tasks = []

with open(yaml_file_name) as f:
    output = yaml.load(f, Loader=yaml.FullLoader)
    tasks = output['tasks'].split()
    for task in tasks:
        print(task)

tasks = "aci"

def run(tasks):
    match tasks:
        case "aci":
            print("aci")
        case "core":
            print("core")
        case _:
            print("not available")

