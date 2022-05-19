from utils.filetools import write_file


class EpgBase():

    def __init__(self, apic=None):
        pass

    
    def build_epg_base_dict(self, apic):
        print()
        print(f'Building {apic.vrf} epg_base_dict...')
        print()
        build_epg_base_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_epg_base_dict_sequence'].split()
        for build_class in build_epg_base_dict_sequence_list:
            apic.vrf_external_epg_base_dict, apic.vrf_internal_epg_base_dict = self.build_epg_base_dict_sub(apic.vrf_external_epg_base_dict, apic.vrf_internal_epg_base_dict, build_class, apic)
        write_file(f'{apic.output_directory}/{apic.vrf_name}_External_EPG_base_parsed.txt', apic.vrf_external_epg_base_dict)
        write_file(f'{apic.output_directory}/{apic.vrf_name}_Internal_EPG_base_parsed.txt', apic.vrf_internal_epg_base_dict)
        return


    def build_epg_base_dict_sub(self, external_parent_dict, internal_parent_dict, build_class, apic):
        for item in apic.data_dict[f'{build_class}_data']:
            if build_class == 'fvATg':
                if 'l3extInstP' in item.keys():
                    item_dn = item['l3extInstP']['attributes']['dn']
                    scope = item['l3extInstP']['attributes']['scope']
                    try:
                        if scope == apic.vrf_scope_dict[apic.vrf]:
                            external_parent_dict.update({item_dn: {}})
                    except KeyError as msg:
                        print()
                        print('=' * 80)
                        print(f'{apic.vrf} in {apic.config.env} is not configured! Exit the program!')
                        print('Encountered KeyError : ', msg)
                        print('=' * 80)
                        print()
                        exit()
                if 'fvAEPg' in item.keys():
                    item_dn = item['fvAEPg']['attributes']['dn']
                    scope = item['fvAEPg']['attributes']['scope']
                    try:
                        if scope == apic.vrf_scope_dict[apic.vrf]:
                            internal_parent_dict.update({item_dn: {}})
                    except KeyError as msg:
                        print()
                        print('=' * 80)
                        print(f'{apic.vrf} in {apic.config.env} is not configured! Exit the program!')
                        print('Encountered KeyError : ', msg)
                        print('=' * 80)
                        print()
                        exit()
        return external_parent_dict, internal_parent_dict
