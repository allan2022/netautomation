import ipaddress
from utils.filetools import write_file
from utils.decorator import calculate_time, decorate_star


class AddEndpoint():

    def __init__(self, apic=None):
        pass


    @decorate_star
    @calculate_time
    def build_add_endpoint_dict(self, apic):
        print()
        print('Building add_endpoint_dict...')
        print()
        build_add_endpoint_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_add_endpoint_dict_sequence'].split()
        for build_class in build_add_endpoint_dict_sequence_list:
            apic.epg_bd_subnet_with_endpoints_dict = self.build_add_endpoint_dict_sub(apic.epg_bd_subnet_with_endpoints_dict, build_class, apic)
        write_file(f'{apic.output_directory}/EPG_BD_to_subnet_with_endpoints_mapping_parsed.txt', apic.epg_bd_subnet_with_endpoints_dict)
        apic.contract_filter_with_endpoints_dict = self.add_endpoint_to_contract_filter(apic.contract_filter_with_endpoints_dict, apic)
        write_file(f'{apic.output_directory}/Contract_Filter_with_endpoints_parsed.txt', apic.contract_filter_with_endpoints_dict)
        return


    def add_endpoint_to_contract_filter(self, parent_dict, apic):
        for key, value in apic.contract_filter_dict.items(): #key is tn-xxxx
            contract_value = value['Contracts']['Standard']
            for sub_key, sub_value in contract_value.items(): #sub_key is uni/tn-xxxx/brc-yyyy
                if '/oobbrc-' not in sub_key:
                    consumer_value = sub_value.get('Consumers')
                    provider_value = sub_value.get('Providers')
                    if consumer_value:
                        for consumer_dn, consumer_sub_value in consumer_value.items(): #epg_bd_subnet_with_endpoints_dict
                            consumer_dn_value = apic.epg_bd_subnet_with_endpoints_dict.get(consumer_dn)
                            parent_dict[key]['Contracts']['Standard'][sub_key]['Consumers'][consumer_dn] = consumer_dn_value
                    if provider_value:
                        for provider_dn, provider_sub_value in provider_value.items(): #epg_bd_subnet_with_endpoints_dict
                            provider_dn_value = apic.epg_bd_subnet_with_endpoints_dict.get(provider_dn)
                            parent_dict[key]['Contracts']['Standard'][sub_key]['Providers'][provider_dn] = provider_dn_value
        return parent_dict


    def build_add_endpoint_dict_sub(self, parent_dict, build_class, apic):
        for item in apic.data_dict[f'{build_class}_data']:
            if build_class == 'fvIp':
                item_dn = item[build_class]['attributes']['dn']
                ip = item_dn.split('/ip-')[-1][1:-1].replace('/32','')
                mac = item_dn.split('/cep-')[-1].split('/')[0]

                if '/BD-' in item_dn:
                    #"uni/ldev-[uni/tn-common/lDevVip-TEST-PA-200_DEVICE]-ctx-[uni/tn-common/ctx-BLUE]-bd-[uni/tn-common/BD-CROSS-TENANT-L4L7BD]/cep-EC:68:81:1A:7B:10/ip-[10.240.103.3]" in lab
                    pass
                elif '/ap-' in item_dn and '/epg-' in item_dn:
                    epg_dn = item_dn.split('/cep-')[0]
                    if parent_dict.get(epg_dn):
                        subnet_list = [*parent_dict[epg_dn].keys()]
                        ip_in_subnet = False
                        for subnet in subnet_list:
                            if ipaddress.ip_address(ip) in ipaddress.ip_network(subnet):
                                parent_dict[epg_dn][subnet].update({ip: {'mac': mac}})
                                ip_in_subnet = True
                        if not ip_in_subnet:
                            parent_dict[epg_dn].update({ip: {'mac': mac}})
                    else:
                        parent_dict.update({epg_dn: {ip: {'mac': mac}}})
                elif '/ctx-' in item_dn:
                    context_name = f"ctx-{item_dn.split('/ctx-')[-1].split('/')[0]}"
                    if context_name == 'ctx-GREEN_VRF':
                        apic.green_vrf_endpoints_dict = {item_dn: 'GREEN_VRF'}
                    if context_name == 'ctx-RED_VRF':
                        apic.red_vrf_endpoints_dict = {item_dn: 'RED_VRF'}
                    if context_name == 'ctx-BLUE_VRF':
                        apic.blue_vrf_endpoints_dict = {item_dn: 'BLUE_VRF'}
                elif '/fabricExtConnP' in item_dn:
                    fabricExtConnP_dn = item_dn.split('/ip-')[0]
                    apic.Fabric_Extension_Connection_dict.update({fabricExtConnP_dn: ip})
                # else:
                #     print('debug fvIp in apicepg ========================')
                #     print(item_dn)
                #     exit()

        return parent_dict
