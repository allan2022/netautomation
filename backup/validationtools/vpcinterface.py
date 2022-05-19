from utils.filetools import write_file
from collections import defaultdict


class VpcInterface():

    def __init__(self, apic=None):
        pass


    def build_vpc_interface_dict(self, apic):
        print()
        print('Building vpc_interface_dict...')
        print()
        vpc_interface_dict = defaultdict(dict)
        build_vpc_interface_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_vpc_interface_dict_sequence'].split()
        for build_class in build_vpc_interface_dict_sequence_list:
            vpc_interface_dict = self.build_vpc_interface_dict_sub(vpc_interface_dict, build_class, apic)
        write_file(f'{apic.output_directory}/VPC_interface_parsed.txt', vpc_interface_dict)
        return


    def build_vpc_interface_dict_sub(self, parent_dict, build_class, apic):
        for item in apic.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']

            if build_class == 'vpcDom':
                peerIp = item[build_class]['attributes']['peerIp']
                vpc_children = item[build_class].get('children')
                if vpc_children:
                    for vpc_child in vpc_children:
                        for key, value in vpc_child.items():
                            if key == 'vpcIf':
                                vpc_interface_name = value['attributes']['fabricPathDn']
                                pcMode = value['attributes']['pcMode']
                                upVlans = value['attributes']['upVlans']
                                usage = value['attributes']['usage']
                                if parent_dict.get(vpc_interface_name):
                                    parent_dict[vpc_interface_name]['vpc domain'].update({item_dn: {'peerIp': peerIp}})
                                else:
                                    parent_dict.update({vpc_interface_name: {'pcMode': pcMode, 'upVlans': upVlans, 'usage': usage, 'vpc domain': {item_dn: {'peerIp': peerIp}}}})

        return parent_dict         
