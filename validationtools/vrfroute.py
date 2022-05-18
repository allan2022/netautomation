from utils.filetools import write_file
from collections import defaultdict


class VrfRoute():

    def __init__(self, apic=None):
        self.route_keyerror_dict = {}
        # self.vrf_route_dict_route_key = defaultdict(dict)
        # self.vrf_route_dict_node_key = defaultdict(dict)


    def build_vrf_route_dict(self, apic):
        print()
        print('Building vrf_route_dict...')
        print()
        build_vrf_route_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_vrf_route_dict_sequence'].split()
        for tenant_vrf_name in apic.tenant_vrf_name_list:
            vrf_route_dict_route_key = defaultdict(dict)
            vrf_route_dict_node_key = defaultdict(dict)
            for build_class in build_vrf_route_dict_sequence_list:
                vrf_route_dict_route_key, vrf_route_dict_node_key = self.build_vrf_route_dict_sub(vrf_route_dict_route_key, vrf_route_dict_node_key, build_class, tenant_vrf_name, apic)
            write_file(f"{apic.output_directory}/routes_{'_'.join(tenant_vrf_name.split(':'))}_route_key_parsed.txt", vrf_route_dict_route_key)
            write_file(f"{apic.output_directory}/routes_{'_'.join(tenant_vrf_name.split(':'))}_node_key_parsed.txt", vrf_route_dict_node_key)
            if self.route_keyerror_dict:
                write_file(f"{apic.output_directory}/issue_route_keyerror_{'_'.join(tenant_vrf_name.split(':'))}_parsed.txt", self.route_keyerror_dict)
        return


    def build_vrf_route_dict_sub(self, vrf_route_dict_route_key, vrf_route_dict_node_key, build_class, tenant_vrf_name, apic):
        if build_class == 'uribv4Route':
            for item in apic.data_dict[f'{build_class}_{tenant_vrf_name}_data']:
                try:
                    item_dn = item[build_class]['attributes']['dn']
                    prefix = item_dn.split('/rt-')[-1][1:-1]
                    pod_node_name = item_dn.split('/sys/uribv4/')[0].replace('topology/', '')
                    if not vrf_route_dict_route_key[prefix].get(pod_node_name):
                        vrf_route_dict_route_key[prefix].update({pod_node_name: defaultdict(dict)})
                    if not vrf_route_dict_node_key[pod_node_name].get(prefix):
                        vrf_route_dict_node_key[pod_node_name].update({prefix: defaultdict(dict)})

                    route_children = item[build_class].get('children')
                    if route_children:
                        for route_child in route_children:
                            for key, value in route_child.items():
                                if key == 'uribv4Nexthop':
                                    nexthop_rn = value['attributes']['rn']
                                    nexthop_addr = value['attributes']['addr']
                                    owner = value['attributes']['owner']
                                    pref = value['attributes']['pref']
                                    routeType = value['attributes']['routeType']
                                    tag = value['attributes']['tag']
                                    metric = value['attributes']['metric']
                                    interface = value['attributes']['if']
                                    active = value['attributes']['active']
                                    vrf_route_dict_route_key[prefix][pod_node_name].update({nexthop_rn: {'nexthop_addr': nexthop_addr, 'owner': owner, 'routeType': routeType, 'preference': pref, 'tag': tag, 'metric': metric, 'interface': interface, 'active': active}})
                                    vrf_route_dict_node_key[pod_node_name][prefix].update({nexthop_rn: {'nexthop_addr': nexthop_addr, 'owner': owner, 'routeType': routeType, 'preference': pref, 'tag': tag, 'metric': metric, 'interface': interface, 'active': active}})
                except KeyError:
                    self.route_keyerror_dict.update({build_class: item})

        return vrf_route_dict_route_key, vrf_route_dict_node_key     
          
