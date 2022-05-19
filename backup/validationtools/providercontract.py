from copy import deepcopy

class ProviderContract():

    def __init__(self, apic=None):
        pass

    
    def build_provider_epg_contract_dict(self, apic):
        print()
        print(f'Building {apic.vrf} {apic.internal_or_external} provider_epg_contract_dict...')
        print()
        epg_contract_dict = deepcopy(apic.vrf_epg_dict)
        build_epg_contract_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_epg_contract_dict_sequence'].split()
        for build_class in build_epg_contract_dict_sequence_list:
            epg_contract_dict = self.build_provider_epg_contract_dict_sub(epg_contract_dict, build_class, apic)
        return epg_contract_dict


    def build_provider_epg_contract_dict_sub(self, parent_dict, build_class, apic):
        for item in apic.data_dict[f'{build_class}_data']:
            if build_class == 'vzBrCP':
                item_dn = item[build_class]['attributes']['dn']
                tenant_name = item_dn.split('/brc-')[0].replace('uni/', '')
                scope = item[build_class]['attributes']['scope']
                contract_children = item[build_class].get('children')

                if contract_children:
                    for contract_child in contract_children:
                        for key, value in contract_child.items():
                            consumer_value = apic.contract_filter_dict[tenant_name]['Contracts']['Standard'][item_dn]['Consumers']
                            subject_value = apic.contract_filter_dict[tenant_name]['Contracts']['Standard'][item_dn]['Subject']
                            if key == 'vzRtProv':
                                provider_dn = value['attributes']['tDn']
                                if provider_dn in apic.vrf_epg_dict.keys():
                                    if parent_dict.get(provider_dn):
                                        parent_dict[provider_dn].update({item_dn: {'scope': scope, 'vzAny': 'no', 'Consumers': consumer_value, 'Subject': subject_value}})
                                    else:
                                        parent_dict.update({provider_dn: {item_dn: {'scope': scope, 'vzAny': 'no', 'Consumers': consumer_value, 'Subject': subject_value}}})
                            if key == 'vzRtAnyToProv' and apic.vrf in value['attributes']['tDn']:
                                # for epg_key, epg_value in apic.vrf_epg_dict.items():
                                for epg_key, _ in apic.vrf_epg_dict.items():
                                    if parent_dict.get(epg_key):
                                        parent_dict[epg_key].update({item_dn: {'scope': scope, 'vzAny': 'yes', 'Consumers': consumer_value, 'Subject': subject_value}})  
                                    else:
                                        parent_dict.update({epg_key: {item_dn: {'scope': scope, 'vzAny': 'no', 'Consumers': consumer_value, 'Subject': subject_value}}})                              
        return parent_dict
