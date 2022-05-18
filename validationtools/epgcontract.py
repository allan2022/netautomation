from utils.filetools import write_file


class EpgContract():

    def __init__(self, apic):
        self.output_directory = apic.output_directory
        self.config = apic.config
        self.data_dict = apic.data_dict

    
    def build_epg_contract_consumer_provider_mapping_dict(self):
        print()
        print(f'Building epg_contract_consumer_provider_mapping_dict...')
        print()
        epg_contract_consumer_provider_mapping_dict = {}
        build_epg_contract_consumer_provider_mapping_sequence_list = self.config.cfg.get('build_dict_sequence')['build_epg_contract_consumer_provider_mapping_dict_sequence'].split()
        for build_class in build_epg_contract_consumer_provider_mapping_sequence_list:
            epg_contract_consumer_provider_mapping_dict = self.build_epg_contract_consumer_provider_mapping_dict_sub(epg_contract_consumer_provider_mapping_dict, build_class)
        write_file(f'{self.output_directory}/EPG_contract_consumer_provider_mapping_parsed.txt', epg_contract_consumer_provider_mapping_dict)


    def build_epg_contract_consumer_provider_mapping_dict_sub(self, parent_dict, build_class):
        for item in self.data_dict[f'{build_class}_data']:
            if build_class == 'vzBrCP':
                contract_dn = item[build_class]['attributes']['dn']
                contract_children = item[build_class].get('children')

                if contract_children:
                    for contract_child in contract_children:
                        for key, value in contract_child.items():
                            if key == 'vzRtProv':
                                provider_dn = value['attributes']['tDn']
                                if parent_dict.get(provider_dn):
                                    parent_dict[provider_dn]['contracts']['provided_contracts'].update({contract_dn:{}})
                                else:
                                    parent_dict.update({provider_dn:{'contracts':{'provided_contracts':{contract_dn:{}}, 'consumed_contracts':{}}}})
                            if key == 'vzRtCons':
                                consumer_dn = value['attributes']['tDn']
                                if parent_dict.get(consumer_dn):
                                    parent_dict[consumer_dn]['contracts']['consumed_contracts'].update({contract_dn:{}})
                                else:
                                    parent_dict.update({consumer_dn:{'contracts':{'provided_contracts':{}, 'consumed_contracts':{contract_dn:{}}}}})
        return parent_dict
