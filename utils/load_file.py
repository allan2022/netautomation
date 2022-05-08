import yaml
import csv
from os.path import exists

def full_load_yaml(yaml_filename = None):
    output = []
    if yaml_filename == None:
        print(f'{yaml_filename} not found!')
    elif not exists(yaml_filename):
        print(f'{yaml_filename} not found!')
    else:
        with open(yaml_filename, 'r') as f:
            output = yaml.load(f, Loader=yaml.FullLoader)
    return output

def full_load_csv(csv_filename = None):
    output = []
    if csv_filename == None:
        print(f'{csv_filename} not found!')
    elif not exists(csv_filename):
        print(f'{csv_filename} not found!')
    else:
        with open(csv_filename, 'r') as f:
            reader = csv.DictReader(f, delimiter = ",")
            for row in reader:
                output.append(row)
    return output

def load_command_csv(csv_filename = None):
    output = []
    if csv_filename == None:
        print(f'{csv_filename} not found!')
    elif not exists(csv_filename):
        print(f'{csv_filename} not found!')
    else:
        with open(csv_filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                output.append(row)
    return output