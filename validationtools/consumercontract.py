from copy import deepcopy

class ConsumerContract():

    def __init__(self, apic=None):
        pass

    
    def build_consumer_epg_contract_dict(self, apic):
        print()
        print(f'Building {apic.vrf} {apic.internal_or_external} consumer_epg_contract_dict...')
        print()
        epg_contract_dict = deepcopy(apic.vrf_epg_dict)
        # epg_contract_with_endpoints_dict = deepcopy(apic.vrf_epg_dict)
        build_epg_contract_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_epg_contract_dict_sequence'].split()
        for build_class in build_epg_contract_dict_sequence_list:
            # epg_contract_dict, epg_contract_with_endpoints_dict = self.build_consumer_epg_contract_dict_sub(epg_contract_dict, epg_contract_with_endpoints_dict, build_class, apic)
            epg_contract_dict = self.build_consumer_epg_contract_dict_sub(epg_contract_dict, build_class, apic)
        # return epg_contract_dict, epg_contract_with_endpoints_dict
        return epg_contract_dict


    # def build_consumer_epg_contract_dict_sub(self, parent_dict, parent_dict_with_endpoints, build_class, apic):
    #     for item in apic.data_dict[f'{build_class}_data']:
    #         if build_class == 'vzBrCP':
    #             item_dn = item[build_class]['attributes']['dn']
    #             tenant_name = item_dn.split('/brc-')[0].replace('uni/', '')
    #             scope = item[build_class]['attributes']['scope']
    #             contract_children = item[build_class].get('children')

    #             if contract_children:
    #                 for contract_child in contract_children:
    #                     for key, value in contract_child.items():
    #                         provider_value = apic.contract_filter_dict[tenant_name]['Contracts']['Standard'][item_dn]['Providers']
    #                         provider_value_with_endpoints = apic.contract_filter_with_endpoints_dict[tenant_name]['Contracts']['Standard'][item_dn]['Providers']
    #                         subject_value = apic.contract_filter_dict[tenant_name]['Contracts']['Standard'][item_dn]['Subject']
    #                         if key == 'vzRtCons':
    #                             consumer_dn = value['attributes']['tDn']
    #                             if consumer_dn in apic.vrf_epg_dict.keys():
    #                             # consumer_vrf = self.epg_vrf_mapping_dict[consumer_dn]['vrf']
    #                             # if consumer_vrf == self.vrf:
    #                                 if parent_dict.get(consumer_dn):
    #                                     parent_dict[consumer_dn].update({item_dn: {'scope': scope, 'vzAny': 'no', 'Providers': provider_value, 'Subject': subject_value}})
    #                                     parent_dict_with_endpoints[consumer_dn].update({item_dn: {'scope': scope, 'vzAny': 'no', 'Providers': provider_value_with_endpoints, 'Subject': subject_value}})
    #                                 else:
    #                                     parent_dict.update({consumer_dn: {item_dn: {'scope': scope, 'vzAny': 'no', 'Providers': provider_value, 'Subject': subject_value}}})
    #                                     parent_dict_with_endpoints.update({consumer_dn: {item_dn: {'scope': scope, 'vzAny': 'no', 'Providers': provider_value_with_endpoints, 'Subject': subject_value}}})
    #                         if key == 'vzRtAnyToCons' and apic.vrf in value['attributes']['tDn']:
    #                             for epg_key, _ in apic.vrf_epg_dict.items():
    #                                 if parent_dict.get(epg_key):
    #                                     parent_dict[epg_key].update({item_dn: {'scope': scope, 'vzAny': 'yes', 'Providers': provider_value, 'Subject': subject_value}})
    #                                     parent_dict_with_endpoints[epg_key].update({item_dn: {'scope': scope, 'vzAny': 'yes', 'Providers': provider_value_with_endpoints, 'Subject': subject_value}})
    #                                 else:
    #                                     parent_dict.update({epg_key: {item_dn: {'scope': scope, 'vzAny': 'yes', 'Providers': provider_value, 'Subject': subject_value}}})
    #                                     parent_dict_with_endpoints.update({epg_key: {item_dn: {'scope': scope, 'vzAny': 'yes', 'Providers': provider_value_with_endpoints, 'Subject': subject_value}}})
    #     return parent_dict, parent_dict_with_endpoints


    def build_consumer_epg_contract_dict_sub(self, parent_dict, build_class, apic):
        for item in apic.data_dict[f'{build_class}_data']:
            if build_class == 'vzBrCP':
                item_dn = item[build_class]['attributes']['dn']
                tenant_name = item_dn.split('/brc-')[0].replace('uni/', '')
                scope = item[build_class]['attributes']['scope']
                contract_children = item[build_class].get('children')

                if contract_children:
                    for contract_child in contract_children:
                        for key, value in contract_child.items():
                            provider_value = apic.contract_filter_dict[tenant_name]['Contracts']['Standard'][item_dn]['Providers']
                            # provider_value_with_endpoints = apic.contract_filter_with_endpoints_dict[tenant_name]['Contracts']['Standard'][item_dn]['Providers']
                            subject_value = apic.contract_filter_dict[tenant_name]['Contracts']['Standard'][item_dn]['Subject']
                            if key == 'vzRtCons':
                                consumer_dn = value['attributes']['tDn']
                                if consumer_dn in apic.vrf_epg_dict.keys():
                                # consumer_vrf = self.epg_vrf_mapping_dict[consumer_dn]['vrf']
                                # if consumer_vrf == self.vrf:
                                    if parent_dict.get(consumer_dn):
                                        parent_dict[consumer_dn].update({item_dn: {'scope': scope, 'vzAny': 'no', 'Providers': provider_value, 'Subject': subject_value}})
                                        # parent_dict_with_endpoints[consumer_dn].update({item_dn: {'scope': scope, 'vzAny': 'no', 'Providers': provider_value_with_endpoints, 'Subject': subject_value}})
                                    else:
                                        parent_dict.update({consumer_dn: {item_dn: {'scope': scope, 'vzAny': 'no', 'Providers': provider_value, 'Subject': subject_value}}})
                                        # parent_dict_with_endpoints.update({consumer_dn: {item_dn: {'scope': scope, 'vzAny': 'no', 'Providers': provider_value_with_endpoints, 'Subject': subject_value}}})
                            if key == 'vzRtAnyToCons' and apic.vrf in value['attributes']['tDn']:
                                for epg_key, _ in apic.vrf_epg_dict.items():
                                    if parent_dict.get(epg_key):
                                        parent_dict[epg_key].update({item_dn: {'scope': scope, 'vzAny': 'yes', 'Providers': provider_value, 'Subject': subject_value}})
                                        # parent_dict_with_endpoints[epg_key].update({item_dn: {'scope': scope, 'vzAny': 'yes', 'Providers': provider_value_with_endpoints, 'Subject': subject_value}})
                                    else:
                                        parent_dict.update({epg_key: {item_dn: {'scope': scope, 'vzAny': 'yes', 'Providers': provider_value, 'Subject': subject_value}}})
                                        # parent_dict_with_endpoints.update({epg_key: {item_dn: {'scope': scope, 'vzAny': 'yes', 'Providers': provider_value_with_endpoints, 'Subject': subject_value}}})
        return parent_dict
