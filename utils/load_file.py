import yaml
import csv
from os.path import exists

csvfilename = "../src/device_inventory.csv"

def full_load_yaml(yaml_filename = None):
    output = None
    if yaml_filename == None:
        print(f'{yaml_filename} not found!')
    elif not exists(yaml_filename):
        print(f'{yaml_filename} not found!')
    else:
        with open(yaml_filename, 'r') as f:
            output = yaml.load(f, Loader=yaml.FullLoader)
    return output

def full_load_csv(csv_filename = csvfilename):
    output = None
    if csv_filename == None:
        print(f'{csv_filename} not found!')
    elif not exists(csv_filename):
        print(f'{csv_filename} not found!')
    else:
        with open(csv_filename, 'r') as f:
            reader = csv.DictReader(f, delimiter = ",")
            for row in reader:
                output.append(row)
    
    print(output)    
    return output


if __name__ == "__main__":
    full_load_csv(csvfilename)    