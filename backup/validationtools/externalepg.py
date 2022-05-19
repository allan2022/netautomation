from utils.filetools import write_file
from acivalidationtools.builddict.buildexternalepgdict import BuildExternalEpgDict


class ExternalEpg():

    def __init__(self, apic):
        self.output_directory = apic.output_directory
        self.config = apic.config
        self.l3extInstP_data_dict = apic.data_dict['l3extInstP_data']
        self.l3extRsEctx_data_dict = apic.data_dict['l3extRsEctx_data']

    
    def build_external_epg_dict(self):
        print()
        print(f'Building build_external_epg_dict...')
        print()
        build_external_epg_dict = BuildExternalEpgDict(self.l3extInstP_data_dict, self.l3extRsEctx_data_dict)
        external_epg_dict = build_external_epg_dict.build_external_epg_dict()
        write_file(f'{self.output_directory}/External_EPG_parsed.txt', external_epg_dict)
