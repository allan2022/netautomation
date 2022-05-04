import csv
from os.path import exists

def full_load_csv(csv_filename = None):
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

    return output