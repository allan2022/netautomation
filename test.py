import os
import yaml


yaml_file_name = "src\all_validation.yaml"
with open(yaml_file_name) as f:
    output = yaml.full_load(f)
    print(output)