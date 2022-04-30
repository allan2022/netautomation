from os.path import exists
import yaml

# yaml_filename = "../src/all_validation.yaml"
# task_list = None

def get_task(yaml_filename = None):
    task_list = None
    task_select = None
    if yaml_filename == None:
        print(f'{yaml_filename} not found!')
    elif not exists(yaml_filename):
        print(f'{yaml_filename} not found!')
    else:
        with open(yaml_filename) as f:
            output = yaml.load(f, Loader=yaml.FullLoader)
            task_list = output['tasks'].split()

        if task_list != None:
            for item in task_list:
                print(f'[{task_list.index(item) + 1}]. {item}')        
            ans = input("Select a task: ")
            task_select = task_list[int(ans)-1]
    return task_list, task_select