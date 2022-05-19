from utils.filetools import write_file
from collections import defaultdict


class OspfNeighbor():

    def __init__(self, apic=None):
        pass

    def build_ospf_neighbor_dict(self, apic):
        print()
        print('Building ospf_neighbor_dict...')
        print()
        ospf_neighbor_dict = defaultdict(dict)
        build_ospf_neighbor_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_ospf_neighbor_dict_sequence'].split()
        for build_class in build_ospf_neighbor_dict_sequence_list:
            ospf_neighbor_dict = self.build_ospf_neighbor_dict_sub(ospf_neighbor_dict, build_class, apic)
        write_file(f'{apic.output_directory}/OSPF_neighbors_parsed.txt', ospf_neighbor_dict)
        return

    def build_ospf_neighbor_dict_sub(self, parent_dict, build_class, apic):
        for item in apic.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']

            if build_class == 'ospfAdjEp':
                if 'dom-overlay-1' not in item_dn:
                    neighbor_id = item[build_class]['attributes']['id']
                    peerIp = item[build_class]['attributes']['peerIp']
                    bfdSt = item[build_class]['attributes']['bfdSt']
                    area = item[build_class]['attributes']['area']
                    parent_dict[item_dn] = {'peerIp': peerIp, 'neighbor id': neighbor_id, 'bfdSt': bfdSt, 'area': area}

        return parent_dict                




