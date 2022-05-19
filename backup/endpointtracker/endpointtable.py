import pandas as pd
from utils.filetools import find_file, read_csv_to_df, write_table
from utils.decorator import calculate_time, decorate_star, sort_ip_in_df, measure_performance
from utils.ipaddresstools import find_index_based_on_ip_mac_timelastseen_in_df
from utils.filetools import get_json_file_data
from utils.generalutils import add_item_to_list_remove_duplicates


class EndpointTable():

    def __init__(self, ep=None):
        self.epg_vrf_mapping_dict = get_json_file_data(ep.latest_baseline_folder, 'EPG_VRF_mapping_parsed.txt', exit=True)


    @measure_performance
    @decorate_star
    def build_endpoint_tracker_table(self, ep):
        """Create or update endpoint_tracker_table for selected ACI Fabric"""

        print()
        print('Executing build_endpoint_tracker_table()...')
        print()
        endpoint_tracker_file = f'{ep.endpoint_tracker_directory}/{ep.config.env}_endpoint_tracker.csv'
        if find_file(endpoint_tracker_file):
            ep.endpoint_tracker_table = read_csv_to_df(endpoint_tracker_file)
            task = 'update endpoint tracker'
        else:
            ep.endpoint_tracker_table = pd.DataFrame(columns=['ip', 'mac', 'tenant', 'ap', 'epg', 'dn', 'interface', 'vrf', 'pod_id', 'node_id', 'timestart', 'timelastseen'])
            task = 'create endpoint tracker'
        build_endpoint_tracker_sequence_list = ep.config.cfg.get('build_dict_sequence')['build_endpoint_tracker_sequence'].split()
        for build_class in build_endpoint_tracker_sequence_list:
            ep.endpoint_tracker_table = self.build_endpoint_tracker_table_sub(ep.endpoint_tracker_table, build_class, ep, task)
        write_table(f'{ep.endpoint_tracker_directory}/{ep.config.env}_endpoint_tracker.csv', ep.endpoint_tracker_table)


    @sort_ip_in_df
    def build_endpoint_tracker_table_sub(self, df, build_class, ep, task):
        for item in ep.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']
            if build_class == 'fvCEp':
                epg_vrf_dn = item_dn.split('/cep-')[0]
                ip = item[build_class]['attributes']['ip']
                mac = item[build_class]['attributes']['mac']
                pod_id = ''
                node_id = []
                interface_list = []
                tenant = ''
                ap = ''
                epg = ''
                interface = ''
                modTs = item[build_class]['attributes']['modTs']
                timestart = modTs.split('.')[0].replace('T', ' ')
                timelastseen = ep.time_str
                ep_children = item[build_class].get('children')
                    
                if '/ctx-' in epg_vrf_dn:
                    tenant = item_dn.split('/tn-')[-1].split('/ctx-')[0]
                    vrf = epg_vrf_dn.replace('uni/', '')
                else:
                    tenant = item_dn.split('/tn-')[-1].split('/ap-')[0]
                    ap = item_dn.split('/ap-')[-1].split('/epg-')[0]
                    epg = item_dn.split('/epg-')[-1].split('/cep-')[0]
                    vrf = self.epg_vrf_mapping_dict[epg_vrf_dn]['vrf']

                if ip != '0.0.0.0':
                    index_list = find_index_based_on_ip_mac_timelastseen_in_df(ip, mac, timelastseen, df)
                    if index_list:
                        df.drop(index=index_list, inplace = True)
                    row = {'ip': ip, 'mac': mac, 'tenant': tenant, 'ap': ap, 'epg': epg, 'dn': epg_vrf_dn, 'vrf': vrf, 'interface': interface_list, 'pod_id': pod_id, 'node_id': node_id, 'timestart': timestart, 'timelastseen': timelastseen}
                    if ep_children:
                        interface_list = []
                        node_id_list = []
                        for ep_child in ep_children:
                            for key, value in ep_child.items():
                                if key == 'fvRsCEpToPathEp': #['fvRsCEpToPathEp', 'fvRsStCEpToPathEp']
                                    interface = value['attributes']['tDn']
                                    interface_list = add_item_to_list_remove_duplicates(interface_list, interface)
                                    pod_id = interface.split('/pod-')[-1].split('/')[0]
                                    row['pod_id'] = pod_id
                                    if '/protpaths-' in interface:
                                        node_ids = interface.split('/protpaths-')[-1].split('/pathep-')[0].split('-')
                                        node_id_list = add_item_to_list_remove_duplicates(node_id_list, node_ids)
                                    if '/paths-' in interface:
                                        node_id = interface.split('/paths-')[-1].split('/pathep-')[0]
                                        node_id_list = add_item_to_list_remove_duplicates(node_id_list, node_id)
                                    if '/pathgrp-' in interface:
                                        pass
                        row['interface'] = interface_list
                        row['node_id'] = node_id_list
                        df = df.append(row, ignore_index=True)

        print(df)
        print('length: ', len(df))
        return df
