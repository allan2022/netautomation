from utils.filetools import write_file
from collections import defaultdict


class EpgVpc():

    def __init__(self, apic=None):
        pass


    def build_epg_vpc_dict(self, apic):
        print()
        print('Building epg_vpc_dict...')
        print()
        epg_vpc_dict = defaultdict(dict)
        build_epg_vpc_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_epg_vpc_dict_sequence'].split()
        for build_class in build_epg_vpc_dict_sequence_list:
            epg_vpc_dict = self.build_epg_vpc_dict_sub(epg_vpc_dict, build_class, apic)
        write_file(f'{apic.output_directory}/EPG_to_VPC_mapping_parsed.txt', epg_vpc_dict)
        return


    def build_epg_vpc_dict_sub(self, parent_dict, build_class, apic):
        for item in apic.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']
            if build_class == 'fvRsPathAtt':
                vpc_name = item[build_class]['attributes']['tDn'].replace('topology/', '')
                epg_name = item_dn.split('/rspathAtt-')[0].replace('uni/', '')
                encap = item[build_class]['attributes']['encap']
                parent_dict[epg_name] = {'vpc': vpc_name, 'encap': encap, 'dn': item_dn}
        return parent_dict
        
