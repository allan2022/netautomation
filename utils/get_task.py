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

if task_list != None:
    for task in task_list:
        print(f'{task_list.index(task) + 1}. {task}')        
    ans = input("Select a task: ")
    print(task_list[int(ans)-1])