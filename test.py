import os
import yaml


yaml_file_name = "src/all_validation.yaml"

with open(yaml_file_name) as f:
    output = yaml.load(f, Loader=yaml.BaseLoader)
    task_list = output['tasks'].split()
    for task in task_list:
        print(task)
