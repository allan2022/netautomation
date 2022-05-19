from acivalidationtools.builddict.buildexternalsubnetdict import BuildExternalSubnetDict
from utils.filetools import write_file


class ExternalSubnet():

    def __init__(self, apic=None):
        self.l3out_in_vrf_list = []
        self.output_directory = apic.output_directory

    
    def build_external_subnet_epg_dict(self, apic):
        print()
        print(f'Building external_subnet_epg_dict...')
        print()

        build_external_subnet_dict = BuildExternalSubnetDict(apic.data_dict['l3extRsEctx_data'], apic.data_dict['l3extSubnet_data'])
        external_subnet_dict = build_external_subnet_dict.build_external_subnet_dict()
        external_subnet_dict_file_name = f'{self.output_directory}/External_subnets_parsed.txt'
        write_file(external_subnet_dict_file_name, external_subnet_dict)
        
        build_external_subnet_epg_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_external_subnet_epg_dict_sequence'].split()
        for build_class in build_external_subnet_epg_dict_sequence_list:
            apic.external_subnet_epg_import_security_no_endpoints_dict, apic.external_subnet_epg_import_security_with_endpoints_dict, apic.external_subnet_epg_import_rtctrl_dict, apic.external_subnet_epg_export_rtctrl_dict, \
                apic.external_subnet_epg_shared_security_dict, apic.external_subnet_epg_shared_rtctrl_dict = \
                self.build_external_subnet_epg_dict_sub(apic.external_subnet_epg_import_security_no_endpoints_dict, apic.external_subnet_epg_import_security_with_endpoints_dict, apic.external_subnet_epg_import_rtctrl_dict, 
                    apic.external_subnet_epg_export_rtctrl_dict, apic.external_subnet_epg_shared_security_dict, apic.external_subnet_epg_shared_rtctrl_dict, build_class, apic)
        return


    def build_external_subnet_epg_dict_sub(self, parent_dict_import_security, parent_dict_import_security_with_endpoints, parent_dict_import_rtctrl, parent_dict_export_rtctrl, parent_dict_shared_security, parent_dict_shared_rtctrl, build_class, apic):
        for item in apic.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']

            if build_class == 'l3extRsEctx':
                l3out_name = item_dn.replace('/rsectx', '')
                vrf_name = item[build_class]['attributes']['tDn'].replace('uni/', '')
                if vrf_name == apic.vrf:
                    self.l3out_in_vrf_list.append(l3out_name)

            if build_class == 'l3extSubnet':
                l3out_name = item_dn.split('/instP')[0]
                if l3out_name in self.l3out_in_vrf_list:
                    if '/out-' in item_dn and '/instP-' in item_dn:
                        external_epg_dn = item_dn.split('/extsubnet-')[0]
                        network_address = item[build_class]['attributes']['ip']
                        scope = item[build_class]['attributes']['scope']

                        if 'import-security' in scope:
                            epg_dict = apic.external_subnet_epg_source_no_endpoints_dict[external_epg_dn]
                            if network_address in parent_dict_import_security.keys():
                                parent_dict_import_security[network_address]['Associated EPG'].update({external_epg_dn: epg_dict})
                            else:
                                parent_dict_import_security.update({network_address: {'Associated EPG': {external_epg_dn: epg_dict}}})
                            epg_dict_with_endpoints = apic.external_subnet_epg_source_with_endpoints_dict[external_epg_dn]
                            if network_address in parent_dict_import_security_with_endpoints.keys():
                                parent_dict_import_security_with_endpoints[network_address]['Associated EPG'].update({external_epg_dn: epg_dict_with_endpoints})
                            else:
                                parent_dict_import_security_with_endpoints.update({network_address: {'Associated EPG': {external_epg_dn: epg_dict_with_endpoints}}})
                        if 'import-rtctrl' in scope:
                            if network_address in parent_dict_import_rtctrl.keys():
                                parent_dict_import_rtctrl[network_address]['Associated EPG'].update({external_epg_dn: scope})
                            else:
                                parent_dict_import_rtctrl.update({network_address: {'Associated EPG': {external_epg_dn: scope}}})
                        if 'export-rtctrl' in scope:
                            if network_address in parent_dict_export_rtctrl.keys():
                                parent_dict_export_rtctrl[network_address]['Associated EPG'].update({external_epg_dn: scope})
                            else:
                                parent_dict_export_rtctrl.update({network_address: {'Associated EPG': {external_epg_dn: scope}}})
                        if 'shared-security' in scope:
                            if network_address in parent_dict_shared_security.keys():
                                parent_dict_shared_security[network_address]['Associated EPG'].update({external_epg_dn: scope})
                            else:
                                parent_dict_shared_security.update({network_address: {'Associated EPG': {external_epg_dn: scope}}}) 
                        if 'shared-rtctrl' in scope:
                            if network_address in parent_dict_shared_rtctrl.keys():
                                parent_dict_shared_rtctrl[network_address]['Associated EPG'].update({external_epg_dn: scope})
                            else:
                                parent_dict_shared_rtctrl.update({network_address: {'Associated EPG': {external_epg_dn: scope}}})                            
                              
        return parent_dict_import_security, parent_dict_import_security_with_endpoints, parent_dict_import_rtctrl, parent_dict_export_rtctrl, parent_dict_shared_security, parent_dict_shared_rtctrl
from acivalidationtools.builddict.buildexternalsubnetdict import BuildExternalSubnetDict
from utils.filetools import write_file


class ExternalSubnet():

    def __init__(self, apic=None):
        self.l3out_in_vrf_list = []
        self.output_directory = apic.output_directory

    
    def build_external_subnet_epg_dict(self, apic):
        print()
        print(f'Building external_subnet_epg_dict...')
        print()

        build_external_subnet_dict = BuildExternalSubnetDict(apic.data_dict['l3extRsEctx_data'], apic.data_dict['l3extSubnet_data'])
        external_subnet_dict = build_external_subnet_dict.build_external_subnet_dict()
        external_subnet_dict_file_name = f'{self.output_directory}/External_subnets_parsed.txt'
        write_file(external_subnet_dict_file_name, external_subnet_dict)
        
        build_external_subnet_epg_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_external_subnet_epg_dict_sequence'].split()
        for build_class in build_external_subnet_epg_dict_sequence_list:
            apic.external_subnet_epg_import_security_no_endpoints_dict, apic.external_subnet_epg_import_security_with_endpoints_dict, apic.external_subnet_epg_import_rtctrl_dict, apic.external_subnet_epg_export_rtctrl_dict, \
                apic.external_subnet_epg_shared_security_dict, apic.external_subnet_epg_shared_rtctrl_dict = \
                self.build_external_subnet_epg_dict_sub(apic.external_subnet_epg_import_security_no_endpoints_dict, apic.external_subnet_epg_import_security_with_endpoints_dict, apic.external_subnet_epg_import_rtctrl_dict, 
                    apic.external_subnet_epg_export_rtctrl_dict, apic.external_subnet_epg_shared_security_dict, apic.external_subnet_epg_shared_rtctrl_dict, build_class, apic)
        return


    def build_external_subnet_epg_dict_sub(self, parent_dict_import_security, parent_dict_import_security_with_endpoints, parent_dict_import_rtctrl, parent_dict_export_rtctrl, parent_dict_shared_security, parent_dict_shared_rtctrl, build_class, apic):
        for item in apic.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']

            if build_class == 'l3extRsEctx':
                l3out_name = item_dn.replace('/rsectx', '')
                vrf_name = item[build_class]['attributes']['tDn'].replace('uni/', '')
                if vrf_name == apic.vrf:
                    self.l3out_in_vrf_list.append(l3out_name)

            if build_class == 'l3extSubnet':
                l3out_name = item_dn.split('/instP')[0]
                if l3out_name in self.l3out_in_vrf_list:
                    if '/out-' in item_dn and '/instP-' in item_dn:
                        external_epg_dn = item_dn.split('/extsubnet-')[0]
                        network_address = item[build_class]['attributes']['ip']
                        scope = item[build_class]['attributes']['scope']

                        if 'import-security' in scope:
                            epg_dict = apic.external_subnet_epg_source_no_endpoints_dict[external_epg_dn]
                            if network_address in parent_dict_import_security.keys():
                                parent_dict_import_security[network_address]['Associated EPG'].update({external_epg_dn: epg_dict})
                            else:
                                parent_dict_import_security.update({network_address: {'Associated EPG': {external_epg_dn: epg_dict}}})
                            epg_dict_with_endpoints = apic.external_subnet_epg_source_with_endpoints_dict[external_epg_dn]
                            if network_address in parent_dict_import_security_with_endpoints.keys():
                                parent_dict_import_security_with_endpoints[network_address]['Associated EPG'].update({external_epg_dn: epg_dict_with_endpoints})
                            else:
                                parent_dict_import_security_with_endpoints.update({network_address: {'Associated EPG': {external_epg_dn: epg_dict_with_endpoints}}})
                        if 'import-rtctrl' in scope:
                            if network_address in parent_dict_import_rtctrl.keys():
                                parent_dict_import_rtctrl[network_address]['Associated EPG'].update({external_epg_dn: scope})
                            else:
                                parent_dict_import_rtctrl.update({network_address: {'Associated EPG': {external_epg_dn: scope}}})
                        if 'export-rtctrl' in scope:
                            if network_address in parent_dict_export_rtctrl.keys():
                                parent_dict_export_rtctrl[network_address]['Associated EPG'].update({external_epg_dn: scope})
                            else:
                                parent_dict_export_rtctrl.update({network_address: {'Associated EPG': {external_epg_dn: scope}}})
                        if 'shared-security' in scope:
                            if network_address in parent_dict_shared_security.keys():
                                parent_dict_shared_security[network_address]['Associated EPG'].update({external_epg_dn: scope})
                            else:
                                parent_dict_shared_security.update({network_address: {'Associated EPG': {external_epg_dn: scope}}}) 
                        if 'shared-rtctrl' in scope:
                            if network_address in parent_dict_shared_rtctrl.keys():
                                parent_dict_shared_rtctrl[network_address]['Associated EPG'].update({external_epg_dn: scope})
                            else:
                                parent_dict_shared_rtctrl.update({network_address: {'Associated EPG': {external_epg_dn: scope}}})                            
                              
        return parent_dict_import_security, parent_dict_import_security_with_endpoints, parent_dict_import_rtctrl, parent_dict_export_rtctrl, parent_dict_shared_security, parent_dict_shared_rtctrl
