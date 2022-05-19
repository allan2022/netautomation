from utils.filetools import write_file
from acivalidationtools.builddict.buildcontractepgdict import BuildContractEpgDict
from acivalidationtools.builddict.buildepgcontractdict import BuildEpgContractDict


class ContractEpg():

    def __init__(self, apic):
        self.output_directory = apic.output_directory
        self.config = apic.config
        self.vzBrCP_data_dict = apic.data_dict['vzBrCP_data']

    
    def build_contract_epg_dict(self):
        print()
        print(f'Building build_contract_epg_dict...')
        print()
        build_contract_epg_dict = BuildContractEpgDict(self.vzBrCP_data_dict)
        contract_epg_dict = build_contract_epg_dict.build_contract_epg_dict()
        write_file(f'{self.output_directory}/Contract_EPG_parsed.txt', contract_epg_dict)
        build_epg_contract_dict = BuildEpgContractDict(self.vzBrCP_data_dict)
        epg_contract_dict = build_epg_contract_dict.build_epg_contract_dict()
        write_file(f'{self.output_directory}/EPG_Contract_parsed.txt', epg_contract_dict)
