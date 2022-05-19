from utils.filetools import write_file
from collections import defaultdict


class VlanPool():

    def __init__(self, apic=None):
        pass


    def build_vlan_pool_dict(self, apic):
        print()
        print('Building vlan_pool_dict...')
        print()
        vlan_pool_dict = defaultdict(dict)
        build_vlan_pool_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_vlan_pool_dict_sequence'].split()
        for build_class in build_vlan_pool_dict_sequence_list:
            vlan_pool_dict = self.build_vlan_pool_dict_sub(vlan_pool_dict, build_class, apic)
        write_file(f'{apic.output_directory}/VLAN_pool_parsed.txt', vlan_pool_dict)
        return


    def build_vlan_pool_dict_sub(self, parent_dict, build_class, apic):
        for item in apic.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']
            if build_class == 'fvnsVlanInstP':
                vlan_children = item[build_class].get('children')
                if vlan_children:
                    for vlan_child in vlan_children:
                        for key, value in vlan_child.items():
                            if key == 'fvnsEncapBlk':
                                pool_name = value['attributes']['rn']
                                full_name = f"{item_dn} {pool_name}"
                                allocMode = item[build_class]['attributes']['allocMode']
                                parent_dict[full_name] = {'allocMode': allocMode}
                            if key == 'fvnsRtVlanNs':
                                domain_name = value['attributes']['tDn']
                                domain_type = value['attributes']['tCl']
                                full_name = f"{item_dn} {domain_name}"
                                parent_dict[full_name] = {'type': domain_type}

        return parent_dict
        
