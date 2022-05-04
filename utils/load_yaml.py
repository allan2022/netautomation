from os.path import exists
import yaml

# file = "../src/core_environment.yaml"


def full_load(yaml_filename = None):
    output = None
    if yaml_filename == None:
        print(f'{yaml_filename} not found!')
    elif not exists(yaml_filename):
        print(f'{yaml_filename} not found!')
    else:
        with open(yaml_filename) as f:
            output = yaml.load(f, Loader=yaml.FullLoader)
            # task_list = output['tasks'].split()
    return output

# if __name__ == "__main__":
#     load()
