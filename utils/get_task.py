import os
import yaml


yaml_filename = "../src/all_validation.yaml"
task_list = None

with open(yaml_filename) as f:
    output = yaml.load(f, Loader=yaml.FullLoader)
    print(output)
    task_list = output['tasks'].split()
    print(task_list)
    for task in task_list:
        print(task)

if not task_list:
    for task in task_list:
        print(f'{task_list.index(task)}. {task}')        