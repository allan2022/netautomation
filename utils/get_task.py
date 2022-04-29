import os
import yaml


yaml_filename = "../src/all_validation.yaml"

with open(yaml_filename) as f:
    output = yaml.load(f, Loader=yaml.FullLoader)
    print(output)
    task_list = output['tasks'].split()
    for task in task_list:
        print(task)