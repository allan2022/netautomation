from utils.filetools import write_file
from acivalidationtools.builddict.buildl3outvrfdict import BuildL3outVrfDict


class L3outVrf():

    def __init__(self, apic):
        self.output_directory = apic.output_directory
        self.config = apic.config
        self.filter_query_dict = apic.data_dict['l3extRsEctx_data']

    
    def build_l3out_vrf_dict(self):
        print()
        print(f'Building build_l3out_vrf_dict...')
        print()
        build_l3out_vrf_dict = BuildL3outVrfDict(self.filter_query_dict)
        l3out_vrf_dict = build_l3out_vrf_dict.build_l3out_vrf_dict()
        write_file(f'{self.output_directory}/L3out_to_VRF_mapping_parsed.txt', l3out_vrf_dict)
