from os.path import exists
import yaml

file = "../src/core_environment.yaml"


def load(yaml_filename = file):
    task_list = None
    if yaml_filename == None:
        print(f'{yaml_filename} not found!')
    elif not exists(yaml_filename):
        print(f'{yaml_filename} not found!')
    else:
        with open(yaml_filename) as f:
            output = yaml.load(f, Loader=yaml.FullLoader)
            print(type(output))
            print(output)
            task_list = output['tasks'].split()
    return task_list

if __name__ == "__main__":
    load()
