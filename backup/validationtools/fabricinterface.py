from utils.filetools import write_file
from collections import defaultdict


class FabricInterface():

    def __init__(self, apic=None):
        pass


    def build_fabric_interface_dict(self, apic):
        print()
        print('Building fabric_interface_dict...')
        print()
        fabric_interface_dict = defaultdict(dict)
        build_fabric_interface_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_fabric_interface_dict_sequence'].split()
        for build_class in build_fabric_interface_dict_sequence_list:
            fabric_interface_dict = self.build_fabric_interface_dict_sub(fabric_interface_dict, build_class, apic)
        write_file(f'{apic.output_directory}/Fabric_interfaces_parsed.txt', fabric_interface_dict)
        return


    def build_fabric_interface_dict_sub(self, parent_dict, build_class, apic):
        for item in apic.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']

            if build_class == 'ethpmPhysIf':
                pod_name = f"pod-{item_dn.split('/pod-')[-1].split('/')[0]}"
                node_name = f"node-{item_dn.split('/node-')[-1].split('/')[0]}"
                interface_name = item_dn.split('/phys-')[-1].replace('/phys', '')[1:-1]
                item_name = f"{pod_name}/{node_name}/{interface_name}"
                accessVlan = item[build_class]['attributes']['accessVlan']
                allowedVlans = item[build_class]['attributes']['allowedVlans']
                lastErrors = item[build_class]['attributes']['lastErrors']
                operMode = item[build_class]['attributes']['operMode']
                operPhyEnSt = item[build_class]['attributes']['operPhyEnSt']
                operSpeed = item[build_class]['attributes']['operSpeed']
                operSt = item[build_class]['attributes']['operSt']
                operVlans = item[build_class]['attributes']['operVlans']
                usage = item[build_class]['attributes']['usage']
                fabric_interface_dict = {'operSt': operSt, 'operPhyEnSt': operPhyEnSt, 'operSpeed': operSpeed, 'operMode': operMode, 'operVlans': operVlans, 'allowedVlans': allowedVlans, 
                                'accessVlan': accessVlan, 'usage': usage, 'lastErrors': lastErrors, 'ethpmPhysIf_dn': item_dn}
                parent_dict[item_name] = fabric_interface_dict

            if build_class == 'l1PhysIf':
                pod_name = f"pod-{item_dn.split('/pod-')[-1].split('/')[0]}"
                node_name = f"node-{item_dn.split('/node-')[-1].split('/')[0]}"
                interface_name = item_dn.split('/phys-')[-1].replace('/phys', '')[1:-1]
                item_name = f"{pod_name}/{node_name}/{interface_name}"
                adminSt = item[build_class]['attributes']['adminSt']
                fcotChannelNumber = item[build_class]['attributes']['fcotChannelNumber']
                layer = item[build_class]['attributes']['layer']
                mode = item[build_class]['attributes']['mode']
                mtu = item[build_class]['attributes']['mtu']
                switchingSt = item[build_class]['attributes']['switchingSt']
                parent_dict[item_name].update({'adminSt': adminSt, 'fcotChannelNumber': fcotChannelNumber, 'layer': layer, 'mode': mode, 'mtu': mtu, 'switchingSt': switchingSt, 'l1PhysIf_dn': item_dn})

        return parent_dict         




