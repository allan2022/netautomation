from utils.filetools import write_file
from acivalidationtools.builddict.buildapplicationepgdict import BuildApplicationEpgDict


class ApplicationEpg():

    def __init__(self, apic):
        self.output_directory = apic.output_directory
        self.config = apic.config
        self.fvAEPg_data_dict = apic.data_dict['fvAEPg_data']
        self.fvCtx_data_dict = apic.data_dict['fvCtx_data']

    
    def build_application_epg_dict(self):
        print()
        print(f'Building build_application_epg_dict...')
        print()
        build_application_epg_dict = BuildApplicationEpgDict(self.fvAEPg_data_dict, self.fvCtx_data_dict)
        application_epg_dict = build_application_epg_dict.build_application_epg_dict()
        write_file(f'{self.output_directory}/Application_EPG_parsed.txt', application_epg_dict)
