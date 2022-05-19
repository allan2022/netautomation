from utils.filetools import write_file


class TopSystem():

    def __init__(self, apic=None):
        pass


    def build_top_system_dict(self, apic):
        print()
        print('Building top_system_dict...')
        print()
        build_top_system_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_top_system_dict_sequence'].split()
        for build_class in build_top_system_dict_sequence_list:
            top_system_dict = self.build_top_system_dict_sub(build_class, apic)
        write_file(f'{apic.output_directory}/top_system_parsed.txt', top_system_dict)


    def build_top_system_dict_sub(self, build_class, apic):
        result_dict = {}
        for item in apic.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']
            if build_class == 'topSystem':
                address = item[build_class]['attributes']['address']
                fabricDomain = item[build_class]['attributes']['fabricDomain']
                fabricId = item[build_class]['attributes']['fabricId']
                inbMgmtAddr = item[build_class]['attributes']['inbMgmtAddr']
                inbMgmtAddrMask = item[build_class]['attributes']['inbMgmtAddrMask']
                inbMgmtGateway = item[build_class]['attributes']['inbMgmtGateway']
                name = item[build_class]['attributes']['name']
                oobMgmtAddr = item[build_class]['attributes']['oobMgmtAddr']
                oobMgmtAddrMask = item[build_class]['attributes']['oobMgmtAddrMask']
                oobMgmtGateway = item[build_class]['attributes']['oobMgmtGateway']
                podId = item[build_class]['attributes']['podId']
                role = item[build_class]['attributes']['role']
                serial = item[build_class]['attributes']['serial']
                state = item[build_class]['attributes']['state']
                if item[build_class]['attributes'].get('version'):
                    version = item[build_class]['attributes']['version']
                else:
                    version = ''
                if item[build_class]['attributes'].get('virtualMode'):
                    virtualMode = item[build_class]['attributes']['virtualMode']
                else:
                    virtualMode = ''
                result_dict.update({
                    item_dn:{
                        'role': role,
                        'name': name,
                        'serial': serial,
                        'version': version,
                        'podId': podId,
                        'fabricId': fabricId,
                        'fabricDomain': fabricDomain,
                        'address': address,
                        'inbMgmtAddr': inbMgmtAddr,
                        'inbMgmtAddrMask': inbMgmtAddrMask,
                        'inbMgmtGateway': inbMgmtGateway,
                        'oobMgmtAddr': oobMgmtAddr,
                        'oobMgmtAddrMask': oobMgmtAddrMask,
                        'oobMgmtGateway': oobMgmtGateway,
                        'state': state,
                        'virtualMode': virtualMode
                    }
                })

        return result_dict    
