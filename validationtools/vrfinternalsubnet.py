from utils.filetools import write_file
from acivalidationtools.builddict.buildvrfinternalsubnetdict import BuildVrfInternalSubnetDict


class VrfInternalSubnet():

    def __init__(self, apic):
        self.output_directory = apic.output_directory
        self.config = apic.config
        self.fvBD_data_dict = apic.data_dict['fvBD_data']

    
    def build_vrf_internal_subnet_dict(self):
        print()
        print(f'Building vrf_internal_subnet_dict...')
        print()
        build_vrf_internal_subnet_dict = BuildVrfInternalSubnetDict(self.fvBD_data_dict)
        vrf_internal_subnet_dict = build_vrf_internal_subnet_dict.build_vrf_internal_subnet_dict()
        write_file(f'{self.output_directory}/VRF_Internal_Subnet_parsed.txt', vrf_internal_subnet_dict)
