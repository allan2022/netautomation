from utils.filetools import write_file
from collections import defaultdict


class FabricNode():

    def __init__(self, apic=None):
        pass


    def build_fabric_node_ip_dict(self, apic):
        print()
        print('Building fabric_node_ip_dict...')
        print()
        fabric_node_ip_dict = defaultdict(dict)
        build_fabric_node_ip_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_fabric_node_ip_dict_sequence'].split()
        for build_class in build_fabric_node_ip_dict_sequence_list:
            fabric_node_ip_dict = self.build_fabric_node_ip_dict_sub(fabric_node_ip_dict, build_class, apic)
        write_file(f'{apic.output_directory}/Fabric_Node_IP_parsed.txt', fabric_node_ip_dict)
        return


    def build_fabric_node_ip_dict_sub(self, parent_dict, build_class, apic):
        for item in apic.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']

            if build_class == 'fabricNode':
                ip = item[build_class]['attributes']['address']
                fabricSt = item[build_class]['attributes']['fabricSt']
                adSt = item[build_class]['attributes']['adSt']
                model = item[build_class]['attributes']['model']
                name = item[build_class]['attributes']['name']
                role = item[build_class]['attributes']['role']
                serial = item[build_class]['attributes']['serial']
                version = item[build_class]['attributes']['version']
                parent_dict.update({ip: {'dn': item_dn, 'fabricSt': fabricSt, 'adSt': adSt, 'model': model, 'name': name, 'role': role, 'serial': serial, 'version': version}})

        return parent_dict         
