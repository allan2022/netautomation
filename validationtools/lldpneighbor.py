from utils.filetools import write_file
from collections import defaultdict


class LldpNeighbor():

    def __init__(self, apic=None):
        pass


    def build_lldp_neighbor_dict(self, apic):
        print()
        print('Building lldp_neighbor...')
        print()
        lldp_neighbor_dict = defaultdict(dict)
        build_lldp_neighbor_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_lldp_neighbor_dict_sequence'].split()
        for build_class in build_lldp_neighbor_dict_sequence_list:
            lldp_neighbor_dict = self.build_lldp_neighbor_dict_sub(lldp_neighbor_dict, build_class, apic)
        write_file(f'{apic.output_directory}/LLDP_neighbors_parsed.txt', lldp_neighbor_dict)
        return


    def build_lldp_neighbor_dict_sub(self, parent_dict, build_class, apic):
        for item in apic.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']

            if build_class == 'lldpAdjEp':
                capability = item[build_class]['attributes']['capability']
                enCap = item[build_class]['attributes']['enCap']
                mgmtIp = item[build_class]['attributes']['mgmtIp']
                mgmtPortMac = item[build_class]['attributes']['mgmtPortMac']
                portDesc = item[build_class]['attributes']['portDesc']
                portIdV = item[build_class]['attributes']['portIdV']
                portVlan = item[build_class]['attributes']['portVlan']
                sysDesc = item[build_class]['attributes']['sysDesc']
                sysName = item[build_class]['attributes']['sysName']
                parent_dict[item_dn] = {'sysName': sysName, 'sysDesc': sysDesc, 'portDesc': portDesc, 'portIdV': portIdV, 'portVlan': portVlan, 'mgmtIp': mgmtIp, 
                                        'mgmtPortMac': mgmtPortMac, 'capability': capability, 'enCap': enCap}

        return parent_dict         




