import pandas as pd
from utils.filetools import write_file, write_table
from copy import deepcopy


class VzAny():

    def __init__(self, apic=None):
        self.vzany_vrf_as_consumer = {}
        self.vzany_vrf_as_provider = {}
        # self.contract_filter_dict = deepcopy(apic.contract_filter_with_endpoints_dict)
        self.contract_filter_dict = deepcopy(apic.contract_filter_no_endpoints_dict)
        self.appcentric_vrf_list = apic.config.cfg.get('appcentric_vrf_list')
        self.vzany_contract_dict = {}


    def build_vzany_dict(self, apic):
        print()
        print('Building vzany_dict...')
        print()
        build_vzany_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_contract_filter_dict_sequence'].split()
        for build_class in build_vzany_dict_sequence_list:
            self.vzany_vrf_as_consumer, self.vzany_vrf_as_provider, self.vzany_contract_dict = self.build_vzany_dict_class_any(self.vzany_vrf_as_consumer, self.vzany_vrf_as_provider, self.vzany_contract_dict, build_class, apic)
        write_file(f'{apic.output_directory}/vzany_vrf_as_consumer_parsed.txt', self.vzany_vrf_as_consumer)
        write_file(f'{apic.output_directory}/vzany_vrf_as_provider_parsed.txt', self.vzany_vrf_as_provider)
        write_file(f'{apic.output_directory}/vzany_contract_parsed.txt', self.vzany_contract_dict)
        self.df_vzany_vrf_as_consumer = self.generate_firewall_request(self.vzany_vrf_as_consumer)
        self.df_vzany_vrf_as_provider = self.generate_firewall_request(self.vzany_vrf_as_provider)
        write_table(f'{apic.output_directory}/vzany_as_consumer_firewall_request.csv', self.df_vzany_vrf_as_consumer)
        write_table(f'{apic.output_directory}/vzany_as_provider_firewall_request_.csv', self.df_vzany_vrf_as_provider)


    def generate_firewall_request(self, vzany_dict):
        df = pd.DataFrame(columns=['source', 'consumer epg', 'destination', 'provider epg', 'contract', 'filter'])
        for key, value in vzany_dict.items():
            if 'consumed contracts' in value.keys():
                source_vrf = key
                contract_dict = value['consumed contracts']
                for contract_key, contract_value in contract_dict.items():
                    contract = contract_key
                    providers_dict = contract_value.get('Providers')
                    filter_dict = contract_value.get('Subject')
                    for _, filter_value in filter_dict.items():
                        filters = filter_value.get('Filters')
                        filter_list = list(filters.keys())
                    if providers_dict:
                        for provider_key, provider_value in providers_dict.items():
                            provider_epg = provider_key
                            if provider_value:
                                ip_subnet_list = list(provider_value.keys())
                            else:
                                ip_subnet_list = []
                            row = {'source': 'to be filled', 'consumer epg': f'{source_vrf}/any', 'destination': ip_subnet_list, 'provider epg': provider_epg, 'contract': contract, 'filter': filter_list}
                            df = df.append(row, ignore_index=True)
            if 'provided contracts' in value.keys():
                destination_vrf = key
                contract_dict = value['provided contracts']
                for contract_key, contract_value in contract_dict.items():
                    contract = contract_key
                    consumers_dict = contract_value.get('Consumers')
                    filter_dict = contract_value.get('Subject')
                    for _, filter_value in filter_dict.items():
                        filters = filter_value.get('Filters')
                        filter_list = list(filters.keys())
                    if consumers_dict:
                        for consumer_key, consumer_value in consumers_dict.items():
                            consumer_epg = consumer_key
                            if consumer_value:
                                ip_subnet_list = list(consumer_value.keys())
                            else:
                                ip_subnet_list = []
                            row = {'source': ip_subnet_list, 'consumer epg': consumer_epg, 'destination': 'to be filled', 'provider epg': f'{destination_vrf}/any', 'contract': contract, 'filter': filter_list}
                            df = df.append(row, ignore_index=True)  
        return df                      



    def build_vzany_dict_class_any(self, vzany_vrf_as_consumer, vzany_vrf_as_provider, vzany_contract_dict, build_class, apic):
        if build_class == 'any':
            for tenant_vrf_name in apic.tenant_vrf_combined_name_list:
                if f'{build_class}_{tenant_vrf_name}_data' in [*apic.data_dict.keys()] and apic.data_dict[f'{build_class}_{tenant_vrf_name}_total'] > 0:
                    for item in apic.data_dict[f'{build_class}_{tenant_vrf_name}_data']:
                        item_dn = item['vzAny']['attributes']['dn'] 
                        vrf_name = item_dn.split('/')[-2]
                        tenant_name = item_dn.split('/')[-3]
                        vrf_full_name = f'{tenant_name}/{vrf_name}'
                        vzAny_children = item['vzAny'].get('children')
                        if vzAny_children:
                            for vzAny_child in vzAny_children:
                                for key, value in vzAny_child.items():
                                    if key == 'vzRsAnyToCons':
                                        if vrf_full_name in self.appcentric_vrf_list:
                                            consumed_contract_name = value['attributes']['tDn']
                                            if vzany_contract_dict.get(consumed_contract_name):
                                                pass
                                            else:
                                                vzany_contract_dict.update({consumed_contract_name: {'vzany': 'yes'}})
                                            contract_cons_dict = self.contract_filter_dict[tenant_name]['Contracts']['Standard'].get(consumed_contract_name)
                                            contract_info = deepcopy(contract_cons_dict)
                                            if contract_info:
                                                contract_info.pop('Consumers')
                                                contract_info.pop('scope')
                                                if contract_info.get('Providers'):
                                                    if f'uni/{vrf_full_name}/any' in contract_info['Providers'].keys():
                                                        contract_info['Providers'].pop(f'uni/{vrf_full_name}/any')
                                                if vzany_vrf_as_consumer.get(vrf_full_name):
                                                    vzany_vrf_as_consumer[vrf_full_name]['consumed contracts'].update({consumed_contract_name: contract_info})
                                                else:
                                                    vzany_vrf_as_consumer.update({vrf_full_name: {'consumed contracts': {consumed_contract_name: contract_info}}})
                                    if key == 'vzRsAnyToProv':
                                        if vrf_full_name in self.appcentric_vrf_list:
                                            provided_contract_name = value['attributes']['tDn']
                                            if vzany_contract_dict.get(provided_contract_name):
                                                pass
                                            else:
                                                vzany_contract_dict.update({provided_contract_name: {'vzany': 'yes'}})
                                            contract_prov_dict = self.contract_filter_dict[tenant_name]['Contracts']['Standard'].get(provided_contract_name)
                                            contract_info = deepcopy(contract_prov_dict)
                                            if contract_info:
                                                contract_info.pop('Providers')
                                                contract_info.pop('scope')
                                                if contract_info.get('Consumers'):
                                                    if f'uni/{vrf_full_name}/any' in contract_info['Consumers'].keys():
                                                        contract_info['Consumers'].pop(f'uni/{vrf_full_name}/any')
                                                if vzany_vrf_as_provider.get(vrf_full_name):
                                                    vzany_vrf_as_provider[vrf_full_name]['provided contracts'].update({provided_contract_name: contract_info})
                                                else:
                                                    vzany_vrf_as_provider.update({vrf_full_name: {'provided contracts': {provided_contract_name: contract_info}}})
        return vzany_vrf_as_consumer, vzany_vrf_as_provider, vzany_contract_dict


    # def build_vzany_dict_class_vzbrcp(self, vzany_vrf_as_consumer, vzany_vrf_as_provider, vzany_epg_as_consumer, vzany_epg_as_provider, build_class, apic):
    #     if build_class == 'vzBrCP':
    #         for item in apic.data_dict[f'{build_class}_data']:
    #             contract_dn = item[build_class]['attributes']['dn']
    #             tenant_name = contract_dn.split('/brc-')[0].replace('uni/', '')
    #             contract_children = item[build_class].get('children')
    #             if contract_children:
    #                 for contract_child in contract_children:
    #                     for key, value in contract_child.items():
    #                         if key == 'vzRtAnyToCons':
    #                             tDn = value['attributes']['tDn']
    #                             if tDn.startswith('uni/') and tDn.endswith('/any'):
    #                                 vrf_full_name = tDn.replace('uni/', '').replace('/any', '')
    #                             else:
    #                                 print('debug VzAny build_vzany_dict_class_vzbrcp vzRtAnyToCons =====================')
    #                                 print(contract_dn)
    #                                 print(key)
    #                                 print(tDn)
    #                                 quit()
    #                             if vrf_full_name in self.appcentric_vrf_list:
    #                                 consumed_contract_name = contract_dn
    #                                 contract_cons_dict = self.contract_filter_dict[tenant_name]['Contracts']['Standard'].get(consumed_contract_name)
    #                                 contract_info = deepcopy(contract_cons_dict)
    #                                 if contract_info:
    #                                     contract_info.pop('Consumers')
    #                                     contract_info.pop('scope')
    #                                     if vzany_vrf_as_consumer.get(vrf_full_name):
    #                                         vzany_vrf_as_consumer[vrf_full_name]['consumed contracts'].update({consumed_contract_name: contract_info})
    #                                     else:
    #                                         vzany_vrf_as_consumer.update({vrf_full_name: {'consumed contracts': {consumed_contract_name: contract_info}}})
    #                         if key == 'vzRtAnyToProv':
    #                             tDn = value['attributes']['tDn']
    #                             if tDn.startswith('uni/') and tDn.endswith('/any'):
    #                                 vrf_full_name = tDn.replace('uni/', '').replace('/any', '')
    #                             else:
    #                                 print('debug VzAny build_vzany_dict_class_vzbrcp vzRtAnyToProv =====================')
    #                                 print(contract_dn)
    #                                 print(key)
    #                                 print(tDn)
    #                                 quit()
    #                             if vrf_full_name in self.appcentric_vrf_list:
    #                                 provided_contract_name = contract_dn
    #                                 contract_prov_dict = self.contract_filter_dict[tenant_name]['Contracts']['Standard'].get(provided_contract_name)
    #                                 contract_info = deepcopy(contract_prov_dict)
    #                                 if contract_info:
    #                                     contract_info.pop('Providers')
    #                                     contract_info.pop('scope')
    #                                     if vzany_vrf_as_provider.get(vrf_full_name):
    #                                         vzany_vrf_as_provider[vrf_full_name]['provided contracts'].update({provided_contract_name: contract_info})
    #                                     else:
    #                                         vzany_vrf_as_provider.update({vrf_full_name: {'provided contracts': {provided_contract_name: contract_info}}})
    #     return vzany_vrf_as_consumer, vzany_vrf_as_provider, vzany_epg_as_consumer, vzany_epg_as_provider

