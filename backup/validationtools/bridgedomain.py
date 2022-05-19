from utils.filetools import write_file
from acivalidationtools.builddict.buildbddict import BuildBdDict


class BridgeDomain():

    def __init__(self, apic):
        self.output_directory = apic.output_directory
        self.config = apic.config
        self.filter_query_dict = apic.data_dict['fvBD_data']

    
    def build_bd_dict(self):
        print()
        print(f'Building build_bd_dict...')
        print()
        build_bd_dict = BuildBdDict(self.filter_query_dict)
        bd_dict = build_bd_dict.build_bd_dict()
        write_file(f'{self.output_directory}/BD_parameters_parsed.txt', bd_dict)
