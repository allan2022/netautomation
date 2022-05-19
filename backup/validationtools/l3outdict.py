from utils.filetools import write_file
from acivalidationtools.builddict.buildl3outdict import BuildL3outDict


class L3outDict():

    def __init__(self, apic):
        self.output_directory = apic.output_directory
        self.config = apic.config
        self.filter_query_dict = apic.data_dict['l3extOut_data']

    
    def build_l3out_dict(self):
        print()
        print(f'Building build_l3out_dict...')
        print()
        build_l3out_dict = BuildL3outDict(self.filter_query_dict)
        l3out_dict = build_l3out_dict.build_l3out_dict()
        write_file(f'{self.output_directory}/L3Out_parsed.txt', l3out_dict)
