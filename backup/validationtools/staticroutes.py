from utils.filetools import write_file


class StaticRoutes():

    def __init__(self, apic=None):
        pass


    def build_static_routes_dict(self, apic):
        print()
        print('Building static_routes_dict...')
        print()
        build_static_routes_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_static_routes_dict_sequence'].split()
        for build_class in build_static_routes_dict_sequence_list:
            static_routes_dict = self.build_static_routes_dict_sub(build_class, apic)
        write_file(f'{apic.output_directory}/static_routes_parsed.txt', static_routes_dict)


    def build_static_routes_dict_sub(self, build_class, apic):
        result_dict = {}
        for item in apic.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']
            if build_class == 'ipRouteP':
                ip_route = item[build_class]['attributes']['ip']
                l3out_dn = item_dn.split('/lnodep-')[0]
                logical_interface_profile = item_dn.split('/lnodep-')[-1].split('/rsnodeL3OutAtt-')[0]
                configured_node = item_dn.split('/rsnodeL3OutAtt-')[-1].split('/rt-')[0][1:-1]
                if apic.l3out_interface_mapping_dict.get(l3out_dn):
                    vrf = apic.l3out_interface_mapping_dict[l3out_dn]['vrf']
                if not result_dict.get(vrf):
                    result_dict.update({vrf:{}})
                if not result_dict[vrf].get(l3out_dn):
                    result_dict[vrf].update({l3out_dn:{}})
                if not result_dict[vrf][l3out_dn].get(ip_route):
                    result_dict[vrf][l3out_dn].update({ip_route:{'logical interface profile':{}}})
                if not result_dict[vrf][l3out_dn][ip_route]['logical interface profile'].get(logical_interface_profile):
                    result_dict[vrf][l3out_dn][ip_route]['logical interface profile'].update({logical_interface_profile:{'nexthop':{}, 'configured nodes':{}}})
                if not result_dict[vrf][l3out_dn][ip_route]['logical interface profile'][logical_interface_profile]['configured nodes'].get(configured_node):
                    result_dict[vrf][l3out_dn][ip_route]['logical interface profile'][logical_interface_profile]['configured nodes'].update({configured_node:{}})

                route_children = item[build_class].get('children')
                if route_children:
                    for route_child in route_children:
                        for key, value in route_child.items():
                            if key == 'ipNexthopP':
                                nexthop = value['attributes']['nhAddr']
                                if not result_dict[vrf][l3out_dn][ip_route]['logical interface profile'][logical_interface_profile]['nexthop'].get(nexthop):
                                    result_dict[vrf][l3out_dn][ip_route]['logical interface profile'][logical_interface_profile]['nexthop'].update({nexthop:{}})

        return result_dict    
