from utils.filetools import write_file
from acivalidationtools.builddict.buildendpointdict import BuildEndpointDict


class EndpointDict():

    def __init__(self, apic):
        self.output_directory = apic.output_directory
        self.config = apic.config
        self.fvBD_data = apic.data_dict['fvBD_data']
        self.fvCEp_data = apic.data_dict['fvCEp_data']

    
    def build_endpoint_dict(self):
        print()
        print(f'Building build_endpoint_dict...')
        print()
        build_endpoint_dict = BuildEndpointDict(self.fvBD_data, self.fvCEp_data)
        endpoint_dict = build_endpoint_dict.build_endpoint_dict()
        write_file(f'{self.output_directory}/Endpoints_parsed.txt', endpoint_dict)
