from collections import defaultdict
from utils.filetools import write_file
from utils.generalutils import dict_reorder


class ConcreteRule():

    def __init__(self, apic=None):
        self.epg_pctag_scope_check_dict = {}
        self.actrlRule_action_check_list = []
        self.vrf_scope_check_dict = {}


    def build_node_access_rule_dict(self, apic):
        print()
        print('Building node_access_rule_dict...')
        print()
        for pod_node_dn in apic.fabric.pod_node_dn_list:
            pod_node_id = pod_node_dn.replace('topology/', '')
            pod_id = pod_node_id.split('/')[0]
            node_id = pod_node_id.split('/')[1]
            node_access_rule_dict = {f'{pod_node_id} Rules': defaultdict(dict)}
            build_node_access_rule_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_node_access_rule_dict_sequence'].split()
            for build_class in build_node_access_rule_dict_sequence_list:
                node_access_rule_dict = self.build_node_access_rule_dict_sub(node_access_rule_dict, build_class, pod_node_id, apic)
            write_file(f'{apic.output_directory}/concrete_access_control_rules_on_{pod_id}_{node_id}_parsed.txt', node_access_rule_dict)
        if self.epg_pctag_scope_check_dict:
            write_file(f'{apic.output_directory}/issue_pctag_scope_to_epg_mapping_parsed.txt', self.epg_pctag_scope_check_dict)


    def build_node_access_rule_dict_sub(self, parent_dict, build_class, pod_node_id, apic):
        if build_class == 'actrlRule':
            query_data = apic.data_dict.get(f'{build_class}_{pod_node_id}_data')
        else:
            query_data = apic.data_dict.get(f'{build_class}_data')
        if query_data:
            for item in query_data:
                if 'error' not in item.keys():
                    item_dn = item[build_class]['attributes'].get('dn')
                    item_name = item_dn.split('/')[-1]
                    if build_class == 'actrlRule':
                        src_epg = ''
                        dst_epg = ''
                        action = item[build_class]['attributes']['action']
                        if 'redir' in action or 'copy' in action or 'no_stats' in action:
                            self.actrlRule_action_check_list.append({item_dn: action})
                        dPcTag = item[build_class]['attributes']['dPcTag']
                        direction = item[build_class]['attributes']['direction']
                        operSt = item[build_class]['attributes']['operSt']
                        rule_id = item[build_class]['attributes']['id']
                        priority = item[build_class]['attributes']['prio']
                        sPcTag = item[build_class]['attributes']['sPcTag']
                        VRFId = item[build_class]['attributes']['scopeId']
                        rule_type = item[build_class]['attributes']['type']
                        filter_id = item[build_class]['attributes']['fltId']
                        name = item[build_class]['attributes']['name']
                        if sPcTag == 'any':
                            src_epg = 'any'
                        # else:
                        #     src_epg = apic.epg.pctag_scope_epg_bd_vrf_dict.get(f'{sPcTag} {VRFId}')
                        #     if not src_epg:
                        #         self.epg_pctag_scope_check_dict.update({item_dn: f'{sPcTag} {VRFId}'})
                        elif 0 <= int(sPcTag) <= 16384:
                            src_epg = apic.epg.pctag_scope_epg_bd_vrf_dict.get(f'{sPcTag}')
                            if not src_epg:
                                self.epg_pctag_scope_check_dict.update({item_dn: f'{sPcTag} {VRFId}'})
                        elif int(sPcTag) > 16384:
                            src_epg = apic.epg.pctag_scope_epg_bd_vrf_dict.get(f'{sPcTag} {VRFId}')
                            if src_epg:
                                if src_epg.startswith('VRF$'):
                                    src_epg = f'{src_epg} - L3Out EPG 0.0.0.0/0 is the source'
                            else:
                                self.epg_pctag_scope_check_dict.update({item_dn: f'{sPcTag} {VRFId}'})
                        else:
                            self.epg_pctag_scope_check_dict.update({item_dn: f'{sPcTag} {VRFId}'})
                            
                        if dPcTag == 'any':
                            dst_epg = 'any'
                        elif 0 <= int(dPcTag) <= 16384:
                            dst_epg = apic.epg.pctag_scope_epg_bd_vrf_dict.get(f'{dPcTag}')
                            if not dst_epg:
                                self.epg_pctag_scope_check_dict.update({item_dn: f'{dPcTag} {VRFId}'})
                        elif int(dPcTag) > 16384:
                            dst_epg = apic.epg.pctag_scope_epg_bd_vrf_dict.get(f'{dPcTag} {VRFId}')
                            if not dst_epg:
                                self.epg_pctag_scope_check_dict.update({item_dn: f'{dPcTag} {VRFId}'})
                        else:
                            self.epg_pctag_scope_check_dict.update({item_dn: f'{dPcTag} {VRFId}'})
                        vrf_name = apic.epg.scope_vrf_dict.get(VRFId)
                        if not vrf_name:
                            self.vrf_scope_check_dict.update({item_dn: VRFId})
                        parent_dict[f'{pod_node_id} Rules'].update({item_name: {'name': name, 'action': action, 'operSt': operSt, 'rule_id': rule_id, 'priority': priority, 'direction': direction, 
                                                                                'sPcTag': sPcTag, 'Src EPG': src_epg, 'dPcTag': dPcTag, 'Dst EPG': dst_epg, 'scopeId': VRFId, 'VRF': vrf_name, 
                                                                                'type': rule_type, 'filter': {'id': filter_id, 'entry': defaultdict(dict)}}})
                    
                    if build_class == 'actrlFlt':
                        pod = f"pod-{item_dn.split('/pod-')[-1].split('/')[0]}"
                        node = f"node-{item_dn.split('/node-')[-1].split('/')[0]}"
                        if f'{pod}/{node}' == pod_node_id:
                            filter_id = item_name.replace('filt-', '-f-')
                            rule_list = [*parent_dict[f'{pod_node_id} Rules'].keys()]
                            related_rules = [rule for rule in rule_list if filter_id in rule]

                            if related_rules:
                                filter_children = item[build_class].get('children')
                                if filter_children:
                                    filter_dict = {}
                                    for filter_child in filter_children:
                                        for key, value in filter_child.items():
                                            if key == 'actrlEntry':
                                                entry_name = value['attributes']['name']
                                                dFromPort = value['attributes']['dFromPort']
                                                dToPort = value['attributes']['dToPort']
                                                etherT = value['attributes']['etherT']
                                                priority = value['attributes']['prio']
                                                protocol = value['attributes']['prot']
                                                sFromPort = value['attributes']['sFromPort']
                                                sToPort = value['attributes']['sToPort']
                                                stateful = value['attributes']['stateful']
                                                tcpRules = value['attributes']['tcpRules']
                                                filter_dict.update({entry_name: {'prototol': protocol, 'sFromPort': sFromPort, 'sToPort': sToPort, 'dFromPort': dFromPort, 'dToPort': dToPort, 
                                                                                    'etherType': etherT, 'stateful': stateful, 'tcpRules': tcpRules}})

                                for rule in related_rules:
                                    parent_dict[f'{pod_node_id} Rules'][rule]['filter']['entry'] = filter_dict

        return parent_dict
