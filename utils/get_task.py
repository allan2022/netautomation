from utils.load_file import full_load_yaml
import yaml

def get_task(yaml_filename, task=None):
    task_list = None
    task_select = None
    output = full_load_yaml(yaml_filename)

    if output != None and task != None:
        task_list = output[task].split()

    if task_list != None:
        print("\n")
        for item in task_list:
            print(f'{task_list.index(item) + 1}. {item}')        
        ans = input("\nSelect a task: ")
        try:
            task_select = task_list[int(ans)-1]
        except (IndexError, ValueError, KeyboardInterrupt):
            task_select = None

    return task_list, task_select