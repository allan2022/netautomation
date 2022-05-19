import pandas as pd
import ipaddress
from collections import defaultdict
from utils.filetools import write_file, write_table
from utils.generalutils import dict_reorder, update_dict, add_item_to_list_remove_duplicates
from utils.dataframetools import df_to_dict_convert
from utils.decorator import calculate_time, decorate_star
from utils.ipaddresstools import find_network_based_on_ip_subnet


class EpgBd():

    def __init__(self, apic=None):
        
        self.aci_tag_scope_dict = {}
        self.scope_pctag_epg_dict = {}
        self.master_epg_list = []
        self.epg_inheritance_dict = {}
        # self.subnets_check_list = []
        self.external_subnets_check_list = []
        self.endpoints_check_list = []
        self.epgs_check_dict = {}
        self.bd_vrf_mapping_dict = {}
        self.bd_keyerror = {}
        self.bd_dict = {}
        self.tag_scope_seg_table = pd.DataFrame(columns=['dn', 'pctag', 'scope', 'seg'])
        self.pctag_scope_epg_bd_vrf_dict = {'0': 'any', '1': 'BD subnet or L3Out logical interface subnet, including SVI', 
                                    '13': 'black_list', '14': 'inter-VRF traffic', '15': 'L3Out EPG with 0.0.0.0/0 subnet'}
        """
        The traffic from class ID 1 to any destination is permitted by an implicit permit rule.
        IPs in a bigger subnet but not in EPG subnet. (an IP in 10.0.0.0/16 is classified L3Out-EPG2, 
        but other IPs in 10.0.0.0/8 are classifed as 13. other IPs will be implicitly dropped.'
        if the L3Out EPG matches only the 0.0.0.0/0 subnet.
        """


    @decorate_star
    @calculate_time
    def build_tenant_networking_epg_dict_table(self, apic):
        print()
        print('Building tenant_networking_epg_dict...')
        print()
        build_tenant_networking_epg_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_tenant_networking_epg_dict_sequence'].split()
        for build_class in build_tenant_networking_epg_dict_sequence_list:
            apic.tenant_networking_epg_dict, self.tag_scope_seg_table = self.build_tenant_networking_epg_dict_table_sub(apic.tenant_networking_epg_dict, self.tag_scope_seg_table, build_class, apic)
        self.tag_scope_seg_table.sort_values(['seg', 'scope', 'pctag', 'dn'], ascending=[True, True, True, True], inplace=True)
        write_file(f'{apic.output_directory}/Tenant_Networking_EPGs_no_Endpoints_parsed.txt', apic.tenant_networking_epg_dict)
        write_table(f'{apic.output_directory}/EPG_VRF_BD_tag_scope_seg_table.csv', self.tag_scope_seg_table)
        self.aci_tag_scope_dict = df_to_dict_convert(df=self.tag_scope_seg_table, column_as_key_list=['dn'], column_as_value_list=['pctag', 'scope','seg'])
        write_file(f'{apic.output_directory}/EPG_VRF_BD_tag_scope_seg_parsed.txt', self.aci_tag_scope_dict)
        self.scope_pctag_epg_dict = df_to_dict_convert(df=self.tag_scope_seg_table, column_as_key_list=['scope', 'pctag'], column_as_value_list=['dn'], column_keyword='dn', item_keyword='/epg- /instP- /inb- /oob-')
        write_file(f'{apic.output_directory}/Scope_pcTag_EPG_dict_parsed.txt', self.scope_pctag_epg_dict)
        write_file(f'{apic.output_directory}/pcTag_Scope_EPG_BD_VRF_mapping_parsed.txt', self.pctag_scope_epg_bd_vrf_dict)
        write_file(f'{apic.output_directory}/EPG_inheritance_mapping_parsed.txt', self.epg_inheritance_dict)
        write_file(f'{apic.output_directory}/Scope_VRF_mapping_parsed.txt', apic.scope_vrf_dict)
        write_file(f'{apic.output_directory}/BD_VRF_mapping_parsed.txt', self.bd_vrf_mapping_dict)
        write_file(f'{apic.output_directory}/EPG_VRF_mapping_parsed.txt', apic.epg_vrf_mapping_dict)
        write_file(f'{apic.output_directory}/EPG_BD_to_subnet_mapping_no_endpoint_parsed.txt', apic.epg_bd_subnet_dict)
        write_file(f'{apic.output_directory}/GREEN_VRF_Endpoints_parsed.txt', apic.green_vrf_endpoints_dict)
        write_file(f'{apic.output_directory}/RED_VRF_Endpoints_parsed.txt', apic.red_vrf_endpoints_dict)
        write_file(f'{apic.output_directory}/BLUE_VRF_Endpoints_parsed.txt', apic.blue_vrf_endpoints_dict)
        write_file(f'{apic.output_directory}/Fabric_Extension_Connection_parsed.txt', apic.Fabric_Extension_Connection_dict)
        write_file(f'{apic.output_directory}/Internal_subnets_to_BD_mapping_parsed.txt', apic.internal_subnet_to_bd_mapping_dict)
        write_file(f'{apic.output_directory}/Internal_subnets_to_EPG_mapping_parsed.txt', apic.internal_subnet_to_epg_mapping_dict)
        write_file(f'{apic.output_directory}/External_subnets_to_EPG_mapping_parsed.txt', apic.external_subnet_to_epg_mapping_dict)
        write_file(f'{apic.output_directory}/External_subnets_to_EPG_per_vrf_mapping_parsed.txt', apic.external_subnet_to_epg_per_vrf_mapping_dict)
        write_file(f'{apic.output_directory}/L3Out_to_interface_mapping_parsed.txt', apic.l3out_interface_mapping_dict)
        self.netcentric_subnets_dict = self.get_netcentric_subnets(apic.epg_bd_subnet_dict)
        write_file(f'{apic.output_directory}/netcentric_subnets_parsed.txt', self.netcentric_subnets_dict)
        write_file(f'{apic.output_directory}/BD_keyerror.txt', self.bd_keyerror)

        # for bd_dn, subnet_dict in apic.epg_bd_subnet_dict.items():
        #     if subnet_dict:
        #         if self.bd_dict.get(bd_dn):
        #             self.bd_dict[bd_dn].update({'subnet': subnet_dict})
        # write_file(f'{apic.output_directory}/BD_parameters_parsed.txt', self.bd_dict)


    def get_netcentric_subnets(self, parent_dict):
        result_dict = {}
        for epg_dn, subnet_dict in parent_dict.items():
            if 'netcentric-supernets' in epg_dn.lower():
                for subnet, _ in subnet_dict.items():
                    if result_dict.get(subnet):
                        result_dict[subnet].update({epg_dn:{}})
                    else:
                        result_dict.update({subnet:{epg_dn:{}}})
        return result_dict


    def add_table_row(self, df, data, build_class):
        if build_class in ['fvAEPg', 'l3extInstP', 'vnsSDEPpInfo', 'vnsREPpInfo', 'mgmtInB', 'mgmtOoB', 'mgmtInstP', 'vnsSDEPpInfo', 'vnsREPpInfo']:
            seg = 0
        else:
            seg = data[build_class]['attributes']['seg']
        if build_class in ['vnsSDEPpInfo', 'vnsREPpInfo']:
            dn = data[build_class]['attributes']['dn']
        else:
            dn = data[build_class]['attributes']['dn'].replace('uni/','')
        pctag = data[build_class]['attributes']['pcTag']
        scope = data[build_class]['attributes']['scope']
        row = [dn, pctag, scope, seg]
        df.loc[df.shape[0]] = row
        return df


    def pctag_scope_epg_bd_vrf_dict_update(self, pctag, scope, name):
        if pctag != 'any' and int(pctag) <= 16384:
            self.pctag_scope_epg_bd_vrf_dict.update({pctag: name})
        else:
            if '/ctx-' in name and '/epg-' not in name:
                self.pctag_scope_epg_bd_vrf_dict.update({f'{pctag} {scope}': f'VRF${name}'})
            if '/bd-' in name and '/epg-' not in name:
                self.pctag_scope_epg_bd_vrf_dict.update({f'{pctag} {scope}': f'BD${name}'})
            else:
                self.pctag_scope_epg_bd_vrf_dict.update({f'{pctag} {scope}': name})


    def build_tenant_networking_epg_dict_table_sub(self, parent_dict, parent_table, build_class, apic):
        df=parent_table
        for item in apic.data_dict[f'{build_class}_data']:
            if build_class != 'fvATg':
                item_dn = item[build_class]['attributes']['dn']
                item_name = item_dn.split('/')[-1]

            if build_class == 'fvTenant':
                if item_name == 'tn-mgmt':
                    parent_dict['Tenants'][item_name] = {'Application Profiles': defaultdict(dict),
                                                    'Networking': {'Bridge Domains': defaultdict(dict), 'VRFs': defaultdict(dict), 'L3Outs': defaultdict(dict)}, 
                                                    'Node Management EPGs': defaultdict(dict), 'External Management Network Instance Profiles': defaultdict(dict)}
                else:
                    parent_dict['Tenants'][item_name] = {'Application Profiles': defaultdict(dict),
                                                    'Networking': {'Bridge Domains': defaultdict(dict), 'VRFs': defaultdict(dict), 'L3Outs': defaultdict(dict)}}
 
            if build_class == 'fvCtx':
                tenant = item_dn.split('/')[-2]
                tn_ctx_name = item_dn.replace('uni/','')
                pcEnfPref = item[build_class]['attributes']['pcEnfPref']
                scope = item[build_class]['attributes']['scope']
                apic.scope_vrf_dict.update({scope: tn_ctx_name})
                apic.vrf_scope_dict.update({tn_ctx_name: scope})
                context_children = item[build_class].get('children')
                prefGrMemb = ''
                if context_children:
                    for context_child in context_children:
                        for key, value in context_child.items():
                            # if key == 'fvRtCtx':
                            #     tCl = value['attributes']['tCl']   #"tCl": "fvBD"
                            #     tDn = value['attributes']['tDn'].replace('uni/','')    #"tDn": "uni/tn-Networks-Playground/BD-NetOps-KO_BD"
                            if key == 'vzAny':
                                prefGrMemb = value['attributes']['prefGrMemb']
                parent_dict['Tenants'][tenant]['Networking']['VRFs'][item_name] = {'scope': scope, 'Policy Control Enforcement Preference': pcEnfPref, 'Preferred Group': prefGrMemb, 'Associated BDs':defaultdict(dict), 'Associated IPs': defaultdict(dict)}
                parent_dict['Tenants'][tenant]['Networking']['VRFs'] = dict_reorder(parent_dict['Tenants'][tenant]['Networking']['VRFs'])
                df = self.add_table_row(parent_table, item, build_class)
                pctag = item[build_class]['attributes']['pcTag']
                self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, tn_ctx_name)

            if build_class == 'fvBD':
                tenant = item_dn.split('/')[-2]

                df = self.add_table_row(parent_table, item, build_class)
                tn_bd_name = item_dn.replace('uni/','')
                pctag = item[build_class]['attributes']['pcTag']
                scope = item[build_class]['attributes']['scope']
                try: 
                    tn_ctx_name = apic.scope_vrf_dict[scope]
                    self.bd_vrf_mapping_dict.update({tn_bd_name: tn_ctx_name})
                    parent_dict['Tenants'][tenant]['Networking']['Bridge Domains'][item_name] = {'vrf': tn_ctx_name, 'Associated IPs': defaultdict(dict), 'Associated Subnets': defaultdict(dict)}
                    parent_dict['Tenants'][tenant]['Networking']['Bridge Domains'] = dict_reorder(parent_dict['Tenants'][tenant]['Networking']['Bridge Domains'])
                    tn_name = tn_ctx_name.split('/')[-2]
                    vrf_name = tn_ctx_name.split('/')[-1]
                    parent_dict['Tenants'][tn_name]['Networking']['VRFs'][vrf_name]['Associated BDs'].update({tn_bd_name: {'Associated Subnets': {}}})
                    self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, tn_bd_name)
                    apic.epg_bd_subnet_dict.update({item_dn: {}})
                except KeyError:
                    self.bd_keyerror.update({item_dn:{'pctag':pctag, 'scope':scope}})
                
                # arpFlood = item[build_class]['attributes']['arpFlood']
                # configIssues = item[build_class]['attributes']['configIssues']
                # epClear = item[build_class]['attributes']['epClear']
                # epMoveDetectMode = item[build_class]['attributes']['epMoveDetectMode']
                # hostBasedRouting = item[build_class]['attributes']['hostBasedRouting']
                # extMngdBy = item[build_class]['attributes']['extMngdBy']
                # intersiteBumTrafficAllow = item[build_class]['attributes']['intersiteBumTrafficAllow']
                # intersiteL2Stretch = item[build_class]['attributes']['intersiteL2Stretch']
                # ipLearning = item[build_class]['attributes']['ipLearning']
                # limitIpLearnToSubnets = item[build_class]['attributes']['limitIpLearnToSubnets']
                # mac = item[build_class]['attributes']['mac']
                # mcastAllow = item[build_class]['attributes']['mcastAllow']
                # multiDstPktAct = item[build_class]['attributes']['multiDstPktAct']
                # name = item[build_class]['attributes']['name']
                # seg = item[build_class]['attributes']['seg']
                # status = item[build_class]['attributes']['status']
                # bd_type = item[build_class]['attributes']['type']
                # unicastRoute = item[build_class]['attributes']['unicastRoute']
                # unkMacUcastAct = item[build_class]['attributes']['unkMacUcastAct']
                # unkMcastAct = item[build_class]['attributes']['unkMcastAct']
                # vmac = item[build_class]['attributes']['vmac']
                # vrf = apic.scope_vrf_dict.get(scope)
                # self.bd_dict.update({item_dn:{
                #     'name': name,
                #     'vrf': vrf,
                #     'ipLearning': ipLearning,
                #     'unicastRoute': unicastRoute,
                #     'limitIpLearnToSubnets': limitIpLearnToSubnets,
                #     'arpFlood': arpFlood,
                #     'configIssues': configIssues,
                #     'epClear': epClear,
                #     'epMoveDetectMode': epMoveDetectMode,
                #     'hostBasedRouting': hostBasedRouting,
                #     'extMngdBy': extMngdBy,
                #     'intersiteBumTrafficAllow': intersiteBumTrafficAllow,
                #     'intersiteL2Stretch': intersiteL2Stretch,
                #     'mac': mac,
                #     'mcastAllow': mcastAllow,
                #     'multiDstPktAct': multiDstPktAct,
                #     'status': status,
                #     'seg': seg,
                #     'pctag': pctag,
                #     'scope': scope,
                #     'type': bd_type,
                #     'unkMacUcastAct': unkMacUcastAct,
                #     'unkMcastAct': unkMcastAct,
                #     'vmac': vmac
                # }})

            if build_class == 'l3extOut':
                tenant = item_dn.split('/')[-2]
                parent_dict['Tenants'][tenant]['Networking']['L3Outs'][item_name] = {'Logical Node Profiles': defaultdict(dict), 'External EPGs': defaultdict(dict)}
                parent_dict['Tenants'][tenant]['Networking']['L3Outs'] = dict_reorder(parent_dict['Tenants'][tenant]['Networking']['L3Outs'])

            if build_class == 'l3extRsEctx':
                l3out_name = f"out-{item_dn.split('/out-')[-1].split('/')[0]}"
                tenant_name = f"tn-{item_dn.split('/tn-')[-1].split('/')[0]}"
                # vrf_name = item[build_class]['attributes']['tDn'].replace('uni/', '')
                vrf_name = item[build_class]['attributes']['tDn']
                parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3out_name].update({'vrf': vrf_name})
                l3out_dn = item_dn.replace('/rsectx', '')
                apic.l3out_interface_mapping_dict.update({l3out_dn: {'vrf': vrf_name, 'interface': {}, 'node id': []}})

            if build_class == 'l3extLNodeP': #lnodep
                l3extOut_name = item_dn.split('/')[-2]
                tenant_name = item_dn.split('/')[-3]
                parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][item_name] = \
                    {'Logical Interface Profiles': defaultdict(dict), 'Configured Nodes': defaultdict(dict), 'BGP Peer Connectivity Profiles': defaultdict(dict)}
                parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'] = \
                    dict_reorder(parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'])

            if build_class == 'l3extLIfP':
                lnodep_name = item_dn.split('/')[-2]
                l3extOut_name = item_dn.split('/')[-3]
                tenant_name = item_dn.split('/')[-4]
                parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][lnodep_name]['Logical Interface Profiles'][item_name] = {'l3extVirtualLIfP': defaultdict(dict)}
                parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][lnodep_name]['Logical Interface Profiles'] = dict_reorder(parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][lnodep_name]['Logical Interface Profiles'])

            if build_class == 'l3extVirtualLIfP':
                item_name = f"vlifp-{item_dn.split('/vlifp-')[-1]}"
                remaining_dn = item_dn.split('/vlifp-')[-2]
                l3extLIfP_name = f"lifp-{remaining_dn.split('/lifp-')[-1]}"
                remaining_dn = remaining_dn.split('/lifp-')[-2]
                lnodep_name = f"lnodep-{remaining_dn.split('/lnodep-')[-1]}"
                remaining_dn = remaining_dn.split('/lnodep-')[-2]
                l3extOut_name = remaining_dn.split('/')[-1]
                tenant_name = remaining_dn.split('/')[-2]
                addr = item[build_class]['attributes']['addr']
                encap = item[build_class]['attributes']['encap']
                encapScope = item[build_class]['attributes']['encapScope']
                ifInstT = item[build_class]['attributes']['ifInstT']
                mac = item[build_class]['attributes']['mac']
                mtu = item[build_class]['attributes']['mtu']
                parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][lnodep_name]['Logical Interface Profiles'][l3extLIfP_name]['l3extVirtualLIfP'][item_name] = \
                    {'addr':addr, 'encap':encap, 'encapScope':encapScope, 'ifInsT':ifInstT, 'mac':mac, 'mtu':mtu, 'l3extRsDynPathAtt': defaultdict(dict), 'BGP Peer Connectivity Profiles': defaultdict(dict)}

            if build_class == 'l3extRsDynPathAtt':
                item_name = f"rsdynPathAtt-{item_dn.split('/rsdynPathAtt-')[-1]}"
                remaining_dn = item_dn.split('/rsdynPathAtt-')[-2]
                l3extVirtualLIfP_name = f"vlifp-{remaining_dn.split('/vlifp-')[-1]}"
                remaining_dn = remaining_dn.split('/vlifp-')[-2]
                l3extLIfP_name = f"lifp-{remaining_dn.split('/lifp-')[-1]}"
                remaining_dn = remaining_dn.split('/lifp-')[-2]
                lnodep_name = f"lnodep-{remaining_dn.split('/lnodep-')[-1]}"
                remaining_dn = remaining_dn.split('/lnodep-')[-2]
                l3extOut_name = remaining_dn.split('/')[-1]
                tenant_name = remaining_dn.split('/')[-2]
                floatingAddr = item[build_class]['attributes']['floatingAddr']
                state = item[build_class]['attributes']['state']
                parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][lnodep_name]['Logical Interface Profiles'][l3extLIfP_name]['l3extVirtualLIfP'][l3extVirtualLIfP_name]['l3extRsDynPathAtt'][item_name] = \
                    {'floatingAddr':floatingAddr, 'state':state}

            if build_class == 'l3extRsNodeL3OutAtt':
                item_name = f"rsnodeL3OutAtt-{item_dn.split('/rsnodeL3OutAtt-')[-1]}"
                lnodep_name = item_dn.split('/rsnodeL3OutAtt-')[-2].split('/')[-1]
                l3extOut_name = item_dn.split('/rsnodeL3OutAtt-')[-2].split('/')[-2]
                tenant_name = item_dn.split('/rsnodeL3OutAtt-')[-2].split('/')[-3]
                rtrId = item[build_class]['attributes']['rtrId']
                rtrIdLoopBack = item[build_class]['attributes']['rtrIdLoopBack']
                pod_id = item_dn.split('/rsnodeL3OutAtt-[topology/pod-')[-1].split('/')[0]
                node_id = item[build_class]['attributes']['tDn'].split('/node-')[-1]
                l3out_dn = item_dn.split('/lnodep-')[0]
                node_id_list = apic.l3out_interface_mapping_dict[l3out_dn]['node id']
                node_id_list = add_item_to_list_remove_duplicates(node_id_list, node_id)
                parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][lnodep_name]['Configured Nodes'].update({item_name: {'router id': rtrId, 'router id loopback': rtrIdLoopBack, 'node id': node_id_list}})
                apic.l3out_interface_mapping_dict[l3out_dn].update({'node id': node_id_list})

            if build_class == 'l3extRsPathL3OutAtt':
                item_name = f"rspathL3OutAtt-{item_dn.split('/rspathL3OutAtt-')[-1]}"
                l3extLIfP_name = item_dn.split('/rspathL3OutAtt-')[-2].split('/')[-1]
                lnodep_name = item_dn.split('/rspathL3OutAtt-')[-2].split('/')[-2]
                l3extOut_name = item_dn.split('/rspathL3OutAtt-')[-2].split('/')[-3]
                tenant_name = item_dn.split('/rspathL3OutAtt-')[-2].split('/')[-4]
                addr = item[build_class]['attributes']['addr']
                encap = item[build_class]['attributes']['encap']
                ifInstT = item[build_class]['attributes']['ifInstT']
                mac = item[build_class]['attributes']['mac']
                parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][lnodep_name]['Logical Interface Profiles'][l3extLIfP_name][item_name] = \
                    {'addr':addr, 'encap':encap, 'ifInstT':ifInstT, 'mac':mac, 'l3extIP':defaultdict(dict), 'BGP Peer Connectivity Profiles': defaultdict(dict)}
                parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][lnodep_name]['Logical Interface Profiles'][l3extLIfP_name] = \
                    dict_reorder(parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][lnodep_name]['Logical Interface Profiles'][l3extLIfP_name])
                l3out_dn = item_dn.split('/lnodep-')[0]
                interface_name = item[build_class]['attributes']['tDn']
                apic.l3out_interface_mapping_dict[l3out_dn]['interface'].update({interface_name: {'addr': addr, 'interface type': ifInstT}})

            if build_class == 'bgpPeerP':
                addr = ''
                adminSt = ''
                peerAsn = ''
                localAsn = ''
                state = ''
                status = ''
                bgpPeerP_children = item[build_class].get('children')
                if bgpPeerP_children:
                    for i in range(len(bgpPeerP_children)):
                        for key, value in bgpPeerP_children[i].items():
                            if key == 'bgpAsP':
                                peerAsn = value['attributes']['asn']
                            if key == 'bgpLocalAsnP':
                                localAsn = value['attributes']['localAsn']
                            if key == 'bgpRsPeerPfxPol':
                                state = value['attributes']['state']
                addr = item[build_class]['attributes']['addr']    
                adminSt = item[build_class]['attributes']['adminSt']
                
                item_name = f"peerP-{item_dn.split('/peerP-')[-1]}"
                remaining_dn = item_dn.split('/peerP-')[-2]

                if '/vlifp-' in item_dn and '/lifp-' in item_dn:
                    l3extVirtualLIfP_name = f"vlifp-{remaining_dn.split('/vlifp-')[-1]}"
                    remaining_dn = remaining_dn.split('/vlifp-')[-2]
                    l3extLIfP_name = f"lifp-{remaining_dn.split('/lifp-')[-1]}"
                    remaining_dn = remaining_dn.split('/lifp-')[-2]
                    lnodep_name = f"lnodep-{remaining_dn.split('/lnodep-')[-1]}"
                    remaining_dn = remaining_dn.split('/lnodep-')[-2]
                    l3extOut_name = remaining_dn.split('/')[-1]
                    tenant_name = remaining_dn.split('/')[-2]                    
                    parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][lnodep_name]['Logical Interface Profiles'][l3extLIfP_name]['l3extVirtualLIfP'][l3extVirtualLIfP_name]['BGP Peer Connectivity Profiles'][item_name] = \
                        {'addr':addr, 'adminSt':adminSt, 'peerAsn':peerAsn, 'localAsn':localAsn, 'state':state}

                elif '/rspathL3OutAtt-' in item_dn:
                    rspathL3OutAtt_name = f"rspathL3OutAtt-{remaining_dn.split('/rspathL3OutAtt-')[-1]}"
                    l3extLIfP_name = remaining_dn.split('/rspathL3OutAtt-')[-2].split('/')[-1]
                    lnodep_name = remaining_dn.split('/rspathL3OutAtt-')[-2].split('/')[-2]
                    l3extOut_name = remaining_dn.split('/rspathL3OutAtt-')[-2].split('/')[-3]
                    tenant_name = remaining_dn.split('/rspathL3OutAtt-')[-2].split('/')[-4]
                    addr = item[build_class]['attributes']['addr']
                    parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][lnodep_name]['Logical Interface Profiles'][l3extLIfP_name][rspathL3OutAtt_name]['BGP Peer Connectivity Profiles'][item_name] = \
                        {'addr':addr, 'adminSt':adminSt, 'peerAsn':peerAsn, 'localAsn':localAsn, 'state':state, 'status':status}
                else:
                    lnodep_name = remaining_dn.split('/')[-1]
                    l3extOut_name = remaining_dn.split('/')[-2]
                    tenant_name = remaining_dn.split('/')[-3]
                    parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][lnodep_name]['BGP Peer Connectivity Profiles'][item_name] = \
                        {'addr':addr, 'adminSt':adminSt, 'peerAsn':peerAsn, 'localAsn':localAsn, 'state':state, 'status':status}
            
            if build_class == 'l3extMember':
                remaining_dn = item_dn.split('/mem-')[-2]
                rspathL3OutAtt_name = f"rspathL3OutAtt-{remaining_dn.split('/rspathL3OutAtt-')[-1]}"
                l3extLIfP_name = remaining_dn.split('/rspathL3OutAtt-')[-2].split('/')[-1]
                lnodep_name = remaining_dn.split('/rspathL3OutAtt-')[-2].split('/')[-2]
                l3extOut_name = remaining_dn.split('/rspathL3OutAtt-')[-2].split('/')[-3]
                tenant_name = remaining_dn.split('/rspathL3OutAtt-')[-2].split('/')[-4]
                addr = item[build_class]['attributes']['addr']
                side = f"Side-{item[build_class]['attributes']['side']} IP"               
                parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][lnodep_name]['Logical Interface Profiles'][l3extLIfP_name][rspathL3OutAtt_name]['l3extIP'][item_name] = {side:addr}
            
            if build_class == 'l3extIp':
                if '/mem-' in item_dn:
                    item_name = f"mem-{item_dn.split('/mem-')[-1].split('/')[0]}"
                    remaining_dn = item_dn.split('/mem-')[-2]
                    rspathL3OutAtt_name = f"rspathL3OutAtt-{remaining_dn.split('/rspathL3OutAtt-')[-1]}"
                    l3extLIfP_name = remaining_dn.split('/rspathL3OutAtt-')[-2].split('/')[-1]
                    lnodep_name = remaining_dn.split('/rspathL3OutAtt-')[-2].split('/')[-2]
                    l3extOut_name = remaining_dn.split('/rspathL3OutAtt-')[-2].split('/')[-3]
                    tenant_name = remaining_dn.split('/rspathL3OutAtt-')[-2].split('/')[-4]
                    addr = item[build_class]['attributes']['addr']
                    parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['Logical Node Profiles'][lnodep_name]['Logical Interface Profiles'][l3extLIfP_name][rspathL3OutAtt_name]['l3extIP'][item_name].update({'Secondary IP':addr})

            if build_class == 'fvAp':
                tenant = item_dn.split('/')[-2]
                parent_dict['Tenants'][tenant]['Application Profiles'][item_name] = defaultdict(dict)
                parent_dict['Tenants'][tenant]['Application Profiles'] = dict_reorder(parent_dict['Tenants'][tenant]['Application Profiles'])

            if build_class == 'fvATg':
                if 'fvAEPg' in item.keys():
                    item_dn = item['fvAEPg']['attributes']['dn']
                    item_name = item_dn.split('/')[-1]
                    application_profile = item_dn.split('/')[-2]
                    tenant = item_dn.split('/')[-3]
                    parent_dict['Tenants'][tenant]['Application Profiles'][application_profile][item_name] = {'Associated IPs': defaultdict(dict), 'Associated Subnets': defaultdict(dict), 'Inheritance': defaultdict(dict)}
                    parent_dict['Tenants'][tenant]['Application Profiles'][application_profile] = dict_reorder(parent_dict['Tenants'][tenant]['Application Profiles'][application_profile])
                    df = self.add_table_row(parent_table, item, 'fvAEPg')
                    tn_epg_name = item_dn.replace('uni/','')
                    pctag = item['fvAEPg']['attributes']['pcTag']
                    scope = item['fvAEPg']['attributes']['scope']
                    if scope == '0':
                        apic.config_issue_check_dict.update({item_dn: {'scope': '0'}})
                    else:
                        tn_ctx_name = apic.scope_vrf_dict[scope]
                        apic.epg_vrf_mapping_dict.update({item_dn: {'vrf': tn_ctx_name}})
                        self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, tn_epg_name)
                        apic.epg_bd_subnet_dict.update({item_dn: {}})
                elif 'l3extInstP' in item.keys():
                    item_dn = item['l3extInstP']['attributes']['dn']
                    item_name = item_dn.split('/')[-1]
                    l3extOut = item_dn.split('/')[-2]
                    tenant = item_dn.split('/')[-3]
                    parent_dict['Tenants'][tenant]['Networking']['L3Outs'][l3extOut]['External EPGs'][item_name] = {'Associated IPs': defaultdict(dict), 'Associated Subnets': defaultdict(dict)}
                    parent_dict['Tenants'][tenant]['Networking']['L3Outs'][l3extOut]['External EPGs'] = \
                        dict_reorder(parent_dict['Tenants'][tenant]['Networking']['L3Outs'][l3extOut]['External EPGs'])
                    df = self.add_table_row(parent_table, item, 'l3extInstP')
                    tn_epg_name = item_dn.replace('uni/','')
                    pctag = item['l3extInstP']['attributes']['pcTag']
                    scope = item['l3extInstP']['attributes']['scope']
                    try:
                        tn_ctx_name = apic.scope_vrf_dict[scope]
                    except KeyError:
                        apic.config_issue_check_dict.update({tn_epg_name: {'scope': scope, 'content': item}})
                    apic.epg_vrf_mapping_dict.update({item_dn: {'vrf': tn_ctx_name}})
                    self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, tn_epg_name)
                    self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, tn_epg_name)
                    apic.epg_bd_subnet_dict.update({item_dn: {}})
                elif 'vnsSDEPpInfo' in item.keys():
                    item_dn = item['vnsSDEPpInfo']['attributes']['dn']
                    encap = item['vnsSDEPpInfo']['attributes']['encap']
                    configSt = item['vnsSDEPpInfo']['attributes']['configSt']
                    df = self.add_table_row(parent_table, item, 'vnsSDEPpInfo')
                    pctag = item['vnsSDEPpInfo']['attributes']['pcTag']
                    scope = item['vnsSDEPpInfo']['attributes']['scope']
                    apic.epg_vrf_mapping_dict.update({item_dn: {'vrf': tn_ctx_name}})
                    self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, tn_epg_name)
                    self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, item_dn)
                    apic.epg_bd_subnet_dict.update({item_dn: {}})
                elif 'vnsREPpInfo' in item.keys():
                    item_dn = item['vnsREPpInfo']['attributes']['dn']
                    encap = item['vnsREPpInfo']['attributes']['encap']
                    configSt = item['vnsREPpInfo']['attributes']['configSt']
                    df = self.add_table_row(parent_table, item, 'vnsREPpInfo')
                    pctag = item['vnsREPpInfo']['attributes']['pcTag']
                    scope = item['vnsREPpInfo']['attributes']['scope']
                    apic.epg_vrf_mapping_dict.update({item_dn: {'vrf': tn_ctx_name}})
                    self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, tn_epg_name)
                    self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, item_dn)
                    apic.epg_bd_subnet_dict.update({item_dn: {}})
                elif 'mgmtInB' in item.keys(): #'dn': 'uni/tn-mgmt/mgmtp-default/inb-IN-BAND'
                    item_dn = item['mgmtInB']['attributes']['dn']
                    item_name = f"inb-{item_dn.split('/inb-')[-1]}"
                    tn_name = f"tn-{item_dn.split('/tn-')[-1].split('/')[0]}"
                    encap = item['mgmtInB']['attributes']['encap']
                    configSt = item['mgmtInB']['attributes']['configSt']
                    parent_dict['Tenants'][tn_name]['Node Management EPGs'][item_name] = {'encap': encap, 'configSt': configSt, 'Associated IPs': defaultdict(dict), 'Associated Subnets': defaultdict(dict)}
                    df = self.add_table_row(parent_table, item, 'mgmtInB')
                    tn_epg_name = item_dn.replace('uni/','')
                    pctag = item['mgmtInB']['attributes']['pcTag']
                    scope = item['mgmtInB']['attributes']['scope']
                    apic.epg_vrf_mapping_dict.update({item_dn: {'vrf': tn_ctx_name}})
                    self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, tn_epg_name)
                    self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, tn_epg_name)
                    apic.epg_bd_subnet_dict.update({item_dn: {}})
                elif 'mgmtOoB' in item.keys(): #"dn": "uni/tn-mgmt/mgmtp-default/oob-default"
                    item_dn = item['mgmtOoB']['attributes']['dn']
                    item_name = f"oob-{item_dn.split('/oob-')[-1]}"
                    tn_name = f"tn-{item_dn.split('/tn-')[-1].split('/')[0]}"
                    configSt = item['mgmtOoB']['attributes']['configSt']
                    parent_dict['Tenants'][tn_name]['Node Management EPGs'][item_name] = {'configSt': configSt, 'Associated IPs': defaultdict(dict), 'Associated Subnets': defaultdict(dict)}
                    df = self.add_table_row(parent_table, item, 'mgmtOoB')
                    tn_epg_name = item_dn.replace('uni/','')
                    pctag = item['mgmtOoB']['attributes']['pcTag']
                    scope = item['mgmtOoB']['attributes']['scope']
                    apic.epg_vrf_mapping_dict.update({item_dn: {'vrf': tn_ctx_name}})
                    self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, tn_epg_name)
                    self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, tn_epg_name)
                    apic.epg_bd_subnet_dict.update({item_dn: {}})
                elif 'mgmtInstP' in item.keys():
                    item_dn = item['mgmtInstP']['attributes']['dn']
                    item_name = f"instp-{item_dn.split('/instp-')[-1]}"
                    tn_name = f"tn-{item_dn.split('/tn-')[-1].split('/')[0]}"
                    configSt = item['mgmtInstP']['attributes']['configSt']
                    parent_dict['Tenants'][tn_name]['External Management Network Instance Profiles'][item_name] = {'configSt': configSt, 'Associated IPs': defaultdict(dict), 'Associated Subnets': defaultdict(dict)}
                    df = self.add_table_row(parent_table, item, 'mgmtInstP')
                    tn_epg_name = item_dn.replace('uni/','')
                    pctag = item['mgmtInstP']['attributes']['pcTag']
                    scope = item['mgmtInstP']['attributes']['scope']
                    apic.epg_vrf_mapping_dict.update({item_dn: {'vrf': tn_ctx_name}})
                    self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, tn_epg_name)
                    self.pctag_scope_epg_bd_vrf_dict_update(pctag, scope, tn_epg_name)
                    apic.epg_bd_subnet_dict.update({item_dn: {}})
                elif 'mgmtInstPDef' in item.keys():
                    pass #same as mgmtInstP
                else:
                    for key, value in item.items():
                        item_dn = value['attributes']['dn']
                        self.epgs_check_dict[item_dn] = item

            if build_class == 'fvRsSecInherited':
                master = f"master-{item_dn.split('/rssecInherited-[uni/')[-1][:-1]}"
                epg_name = item_dn.split('/rssecInherited-[uni/')[-0].split('/')[-1]
                #if '/ap-' in item_dn: (TODO for non ap)
                ap_name = item_dn.split('/rssecInherited-[uni/')[-0].split('/')[-2]
                tn_name = item_dn.split('/rssecInherited-[uni/')[-0].split('/')[-3]
                state = item[build_class]['attributes']['state']
                parent_dict['Tenants'][tn_name]['Application Profiles'][ap_name][epg_name]['Inheritance'][master] = {'state': state}
                self.master_epg_list.append(master)
                self.epg_inheritance_dict.update({master: f'{tn_name}/{ap_name}/{epg_name}'})

            
            if build_class == 'fvSubnet':
                item_name = f"subnet-{item_dn.split('/subnet-')[-1]}"
                scope = item[build_class]['attributes']['scope']
                if '/BD-' in item_dn:
                    bd_name = item_dn.split('/subnet-')[-2].split('/')[-1]
                    tenant = item_dn.split('/BD-')[-2].split('/')[-1]
                    try:
                        parent_dict['Tenants'][tenant]['Networking']['Bridge Domains'][bd_name]['Associated Subnets'][item_name] = {'scope':scope}
                        parent_dict['Tenants'][tenant]['Networking']['Bridge Domains'][bd_name]['Associated Subnets'] = dict_reorder(parent_dict['Tenants'][tenant]['Networking']['Bridge Domains'][bd_name]['Associated Subnets'])
                        tn_bd_name = item_dn.split('/subnet-')[-2].replace('uni/', '')
                        tn_ctx_name = self.bd_vrf_mapping_dict[tn_bd_name]
                        tn_name = tn_ctx_name.split('/')[0]
                        ctx_name = tn_ctx_name.split('/')[-1]
                        parent_dict['Tenants'][tn_name]['Networking']['VRFs'][ctx_name]['Associated BDs'][tn_bd_name]['Associated Subnets'].update({item_dn.replace('uni/', ''): {}})
                        bd_dn = item_dn.split('/subnet-')[0]
                        subnet = item_dn.split('/subnet-')[-1][1:-1]
                        network = find_network_based_on_ip_subnet(subnet)
                        network = str(ipaddress.ip_network(network, strict=False))
                        apic.epg_bd_subnet_dict = update_dict(apic.epg_bd_subnet_dict, bd_dn, network)
                        apic.internal_subnet_to_bd_mapping_dict.update({network: {'bd': {bd_dn: {'vrf': ctx_name}}}})
                    except KeyError:
                        self.bd_keyerror.update({item_dn:{'scope':scope}})

                elif '/ap-' in item_dn and '/epg-' in item_dn:
                    application_epg = item_dn.split('/subnet-')[-2].split('/')[-1]
                    application_profile = item_dn.split('/subnet-')[-2].split('/')[-2]
                    tenant = item_dn.split('/subnet-')[-2].split('/')[-3]
                    parent_dict['Tenants'][tenant]['Application Profiles'][application_profile][application_epg]['Associated Subnets'][item_name] = {'scope':scope}
                    parent_dict['Tenants'][tenant]['Application Profiles'][application_profile][application_epg]['Associated Subnets'] = dict_reorder(parent_dict['Tenants'][tenant]['Application Profiles'][application_profile][application_epg]['Associated Subnets'])
                    epg_dn = item_dn.split('/subnet-')[0]
                    subnet = item_dn.split('/subnet-')[-1][1:-1]
                    network = find_network_based_on_ip_subnet(subnet)
                    network = str(ipaddress.ip_network(network, strict=False))
                    apic.epg_bd_subnet_dict = update_dict(apic.epg_bd_subnet_dict, epg_dn, network)  
                    epg_vrf = apic.epg_vrf_mapping_dict[epg_dn].get('vrf')
                    apic.internal_subnet_to_epg_mapping_dict.update({network: {'epg': {epg_dn: {'vrf': epg_vrf}}}})
                else:
                    print('debug fvSubnet in apicepg ========================')
                    print(item_dn)
                    exit()
                    # self.subnets_check_list.append(item_dn)

            if build_class == 'l3extSubnet':
                item_name = f"extsubnet-{item_dn.split('/extsubnet-')[-1]}"
                remaining_dn = item_dn.split('/extsubnet-')[-2]
                if '/out-' in item_dn and '/instP-' in item_dn:
                    external_epg_name = f"instP-{remaining_dn.split('/instP-')[-1]}"
                    remaining_dn = remaining_dn.split('/instP-')[-2]
                    l3extOut_name = f"out-{remaining_dn.split('/out-')[-1]}"
                    remaining_dn = remaining_dn.split('/out-')[-2]
                    tenant_name = f"tn-{remaining_dn.split('/tn-')[-1]}"
                    
                    scope = item[build_class]['attributes']['scope']
                    parent_dict['Tenants'][tenant_name]['Networking']['L3Outs'][l3extOut_name]['External EPGs'][external_epg_name]['Associated Subnets'][item_name] = \
                        {'scope':scope}
                    epg_dn = item_dn.split('/extsubnet-')[0]
                    network = item[build_class]['attributes']['ip']
                    network = str(ipaddress.ip_network(network, strict=False))
                    apic.epg_bd_subnet_dict = update_dict(apic.epg_bd_subnet_dict, epg_dn, network)
                    epg_vrf = apic.epg_vrf_mapping_dict[epg_dn].get('vrf')
                    if apic.external_subnet_to_epg_mapping_dict.get(network):
                        apic.external_subnet_to_epg_mapping_dict[network]['epg'].update({epg_dn: {'vrf': epg_vrf, 'scope': scope}})
                    else:
                        apic.external_subnet_to_epg_mapping_dict.update({network: {'epg': {epg_dn: {'vrf': epg_vrf, 'scope': scope}}}})
                    if apic.external_subnet_to_epg_per_vrf_mapping_dict.get(epg_vrf):
                        if apic.external_subnet_to_epg_per_vrf_mapping_dict[epg_vrf].get(network):
                            apic.external_subnet_to_epg_per_vrf_mapping_dict[epg_vrf][network]['epg'].update({epg_dn: {'vrf': epg_vrf, 'scope': scope}})
                        else:
                            apic.external_subnet_to_epg_per_vrf_mapping_dict[epg_vrf].update({network: {'epg': {epg_dn: {'scope': scope}}}})
                    else:
                        apic.external_subnet_to_epg_per_vrf_mapping_dict.update({epg_vrf: {network: {'epg': {epg_dn: {'scope': scope}}}}})
                elif '/fabricExtConnP-' in item_dn:
                    print('debug fabricExtConnP ========================')
                    print(item)
                    
                    fabricExtConnP_dn = item_dn.split('/extsubnet-')[0]
                    network = item[build_class]['attributes']['ip']
                    network = str(ipaddress.ip_network(network, strict=False))
                    apic.Fabric_Extension_Connection_dict.update({fabricExtConnP_dn: network})
                    epg_vrf = apic.epg_vrf_mapping_dict.get(fabricExtConnP_dn)
                    scope = item[build_class]['attributes']['scope']
                    if apic.external_subnet_to_epg_mapping_dict.get(network):
                        apic.external_subnet_to_epg_mapping_dict[network][network]['epg'].update({fabricExtConnP_dn: {'vrf': epg_vrf, 'scope': scope}})
                    else:
                        apic.external_subnet_to_epg_mapping_dict.update({network: {'epg': {fabricExtConnP_dn: {'vrf': epg_vrf, 'scope': scope}}}})
                    if apic.external_subnet_to_epg_per_vrf_mapping_dict.get(epg_vrf):
                        if apic.external_subnet_to_epg_per_vrf_mapping_dict[epg_vrf].get(network):
                            apic.external_subnet_to_epg_per_vrf_mapping_dict[epg_vrf][network]['epg'].update({fabricExtConnP_dn: {'vrf': epg_vrf, 'scope': scope}})
                        else:
                            apic.external_subnet_to_epg_per_vrf_mapping_dict[epg_vrf].update({network: {'epg': {fabricExtConnP_dn: {'scope': scope}}}})
                    else:
                        apic.external_subnet_to_epg_per_vrf_mapping_dict.update({epg_vrf: {network: {'epg': {fabricExtConnP_dn: {'scope': scope}}}}})
                else:
                    print('debug l3extSubnet in epgbd ========================')
                    print(item_dn)
                    exit()

        return parent_dict, df
