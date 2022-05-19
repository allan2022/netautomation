from utils.filetools import write_file
from collections import defaultdict


class BgpPeer():

    def __init__(self, apic=None):
        pass

    def build_bgp_peer_dict(self, apic):
        print()
        print('Building bgp_peer_dict...')
        print()
        bgp_peer_dict = defaultdict(dict)
        build_bgp_peer_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_bgp_peer_dict_sequence'].split()
        for build_class in build_bgp_peer_dict_sequence_list:
            bgp_peer_dict = self.build_bgp_peer_dict_sub(bgp_peer_dict, build_class, apic)
        write_file(f'{apic.output_directory}/BGP_peers_parsed.txt', bgp_peer_dict)
        return

    def build_bgp_peer_dict_sub(self, parent_dict, build_class, apic):
        for item in apic.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']
            if build_class == 'bgpPeerEntry':
                if 'dom-overlay-1' not in item_dn:
                    operSt = item[build_class]['attributes']['operSt']
                    rtrId = item[build_class]['attributes']['rtrId']
                    bgp_type = item[build_class]['attributes']['type']
                    
                    bgp_peer_children = item[build_class].get('children')
                    if bgp_peer_children:
                        for bgp_peer_child in bgp_peer_children:
                            for key, value in bgp_peer_child.items():
                                if key == 'bgpPeerAfEntry':
                                    address_family_type = value['attributes']['type']
                                    if address_family_type == 'ipv4-ucast':
                                        acceptedPaths = int(value['attributes']['acceptedPaths'])
                                        pfxSent = int(value['attributes']['pfxSent'])
                                        parent_dict[item_dn] = {'operSt': operSt, 'rtrId': rtrId, 'type': bgp_type, 'ipv4-ucast-received_routes': acceptedPaths, 'ipv4-ucast-advertised_routes': pfxSent}

        return parent_dict                
