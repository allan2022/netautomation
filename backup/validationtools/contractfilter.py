from collections import defaultdict
from utils.filetools import write_file
from utils.generalutils import dict_reorder


class ContractFilter():

    def __init__(self, apic=None):
        self.endpoints_check_list = []
        self.filter_check_list = []
        self.filter_check_dict = {}
        self.vzentry_check_list = []
        self.vzentry_check_dict = {}
        self.subject_check_list = []
        self.subject_check_dict = {}
        self.subject_and_filter_tdn_check_list = []
        self.subject_and_filter_tdn_check_dict = {}
        self.contract_check_list = []
        self.contract_check_dict = {}


    def build_contract_filter_dict(self, apic):
        print()
        print('Building contract_filter_dict...')
        print()
        build_contract_filter_dict_sequence_list = apic.config.cfg.get('build_dict_sequence')['build_contract_filter_dict_sequence'].split()
        for build_class in build_contract_filter_dict_sequence_list:
            apic.contract_filter_dict = self.build_contract_filter_dict_sub(apic.contract_filter_dict, build_class, apic)
        write_file(f'{apic.output_directory}/Contract_Filter_no_endpoint_parsed.txt', apic.contract_filter_dict)
        return


    def build_contract_filter_dict_sub(self, parent_dict, build_class, apic):
        if build_class != 'any':
            for item in apic.data_dict[f'{build_class}_data']:
                item_dn = item[build_class]['attributes']['dn']
                item_name = item_dn.split('/')[-1]

                if build_class == 'fvTenant':
                    parent_dict[item_name] = {'VRFs': defaultdict(dict), 
                                                        'Contracts': {'Standard': defaultdict(dict), 'Filters': defaultdict(dict)}}

                if build_class == 'vzFilter':
                    tenant = item_dn.split('/')[-2]
                    try:
                        parent_dict[tenant]['Contracts']['Filters'][item_dn] = defaultdict(dict)
                    except KeyError:
                        self.filter_check_list.append(item_dn)
                        self.filter_check_dict[item_dn] = item

                if build_class == 'vzEntry':
                    filter_name = item_dn.split('/')[-2]
                    tenant_name = item_dn.split('/')[-3]
                    dFromPort = item[build_class]['attributes']['dFromPort']
                    dToPort = item[build_class]['attributes']['dToPort']
                    prot = item[build_class]['attributes']['prot']
                    sFromPort = item[build_class]['attributes']['sFromPort']
                    sToPort = item[build_class]['attributes']['sToPort']
                    stateful = item[build_class]['attributes']['stateful']
                    etherT = item[build_class]['attributes']['etherT']
                    try:
                        parent_dict[tenant_name]['Contracts']['Filters'][filter_name][item_dn] = \
                            {'prot':prot,'dFromPort':dFromPort, 'dToPort':dToPort, 'sFromPort':sFromPort, 'sToPort':sToPort, 'etherType': etherT, 'stateful': stateful}
                    except KeyError:
                        self.vzentry_check_list.append(item_dn)
                        self.vzentry_check_dict[item_dn] = item

                if build_class == 'vzBrCP':
                    tenant_name = item_dn.split('/')[-2]
                    scope = item[build_class]['attributes']['scope']
                    consumer_dict = {}
                    provider_dict = {}
                    contract_children = item[build_class].get('children')
                    if contract_children:
                        for contract_child in contract_children:
                            for key, value in contract_child.items():
                                if key in ['vzRtCons', 'vzRtAnyToCons']:
                                    consumer_dn = value['attributes']['tDn']
                                    consumer_dict.update({consumer_dn: apic.epg_bd_subnet_dict[consumer_dn]})
                                    if f'master-{consumer_dn}' in apic.epg.master_epg_list:
                                        inheritance_epg_dn = apic.epg.epg_inheritance_dict[f'master-{consumer_dn}']
                                        consumer_dict.update({inheritance_epg_dn: f'inherted from {consumer_dn}'})
                                if key in ['vzRtProv', 'vzRtAnyToProv']:
                                    provider_dn = value['attributes']['tDn']
                                    provider_dict.update({provider_dn: apic.epg_bd_subnet_dict[provider_dn]})
                                    if f'master-{provider_dn}' in apic.epg.master_epg_list:
                                        inheritance_epg_dn = apic.epg.epg_inheritance_dict[f'master-{provider_dn}']
                                        provider_dict.update({inheritance_epg_dn: f'inherited from {provider_dn}'})
                    try:
                        parent_dict[tenant_name]['Contracts']['Standard'][item_dn] = {'scope':scope, 'Consumers':consumer_dict, 'Providers':provider_dict, 'Subject': defaultdict(dict)}
                    except KeyError:
                        self.contract_check_list.append(item_dn)
                        self.contract_check_dict[item_dn] = item

                if build_class == 'vzSubj':
                    brc_dn = item_dn.split('/subj-')[0]
                    tenant = item_dn.split('/')[-3]
                    try:
                        parent_dict[tenant]['Contracts']['Standard'][brc_dn]['Subject'][item_dn] = {'Filters': defaultdict(dict)}
                    except KeyError:
                        self.subject_check_list.append(item_dn)
                        self.subject_check_dict[item_dn] = item

                    vzSubj_children = item[build_class].get('children')
                    if vzSubj_children:
                        for vzSubj_child in vzSubj_children:
                            for key, value in vzSubj_child.items():
                                if key == 'vzRsSubjFiltAtt' or key == 'vzRsSubjGraphAtt':
                                    tDn = value['attributes']['tDn']
                                    tRn = value['attributes']['tRn']
                                    state = value['attributes']['state']
                                    if tDn:
                                        # filter_name = tDn.replace('uni/','')
                                        filter_name = tDn
                                    else:
                                        filter_name = tRn
                                    action = value['attributes'].get('action')
                                    try:
                                        if state != 'formed':
                                            parent_dict[tenant]['Contracts']['Standard'][brc_dn]['Subject'][item_dn]['Filters'].update({filter_name: {'state':state}})
                                        else:
                                            parent_dict[tenant]['Contracts']['Standard'][brc_dn]['Subject'][item_dn]['Filters'].update({filter_name: {}})
                                    except KeyError:
                                        self.subject_and_filter_tdn_check_list.append({filter_name:{brc_dn:item_dn}})
                                        self.subject_and_filter_tdn_check_dict[filter_name] = value

                if build_class == 'vzRsFiltAtt': #Interm (consumer to provider) and Outterm (provider to consumer) filters
                    if '/intmnl/rsfiltAtt-' in item_dn:
                        item_name = f"ConsumerToProvider-InTerm-flt-{item_dn.split('/intmnl/rsfiltAtt-')[-1]}"
                        subj_dn = item_dn.split('/intmnl/')[0]
                        
                    if '/outtmnl/rsfiltAtt-' in item_dn:
                        item_name = f"ProviderToConsumer-OutTerm-flt-{item_dn.split('/outtmnl/rsfiltAtt-')[-1]}"
                        subj_dn = item_dn.split('/outtmnl/')[0]
                    brc_dn = item_dn.split('/subj-')[0]
                    tn_name = f"tn-{item_dn.split('/tn-')[-1].split('/')[0]}"
                    action = item[build_class]['attributes']['action']
                    parent_dict[tn_name]['Contracts']['Standard'][brc_dn]['Subject'][subj_dn]['Filters'].update({item_name: {'action':action, 'dn': item_dn}})

        else: # vzAny build_class == 'any'
            for tenant_vrf_name in apic.tenant_vrf_combined_name_list:
                if f'{build_class}_{tenant_vrf_name}_data' in [*apic.data_dict.keys()] and apic.data_dict[f'{build_class}_{tenant_vrf_name}_total'] > 0:
                    for item in apic.data_dict[f'{build_class}_{tenant_vrf_name}_data']:
                        item_dn = item['vzAny']['attributes']['dn'] 
                        vrf_name = item_dn.split('/')[-2]
                        tenant_name = item_dn.split('/')[-3]
                        if not parent_dict.get(tenant_name):
                            parent_dict.update({tenant_name: {'VRFs': defaultdict(dict)}})
                        if vrf_name not in [*parent_dict[tenant_name]['VRFs'].keys()]:
                            parent_dict[tenant_name]['VRFs'].update({vrf_name: {'vzAny': {'Consumed Contracts': defaultdict(dict), 'Provided Contracts': defaultdict(dict)}}})
                        vzAny_children = item['vzAny'].get('children')
                        if vzAny_children:
                            for vzAny_child in vzAny_children:
                                for key, value in vzAny_child.items():
                                    if key == 'vzRsAnyToCons':
                                        # consumed_contract_name = value['attributes']['tDn'].replace('uni/', '')
                                        consumed_contract_name = value['attributes']['tDn']
                                        parent_dict[tenant_name]['VRFs'][vrf_name]['vzAny']['Consumed Contracts'].update({consumed_contract_name: {}})
                                    if key == 'vzRsAnyToProv':
                                        # provided_contract_name = value['attributes']['tDn'].replace('uni/', '')
                                        provided_contract_name = value['attributes']['tDn']
                                        parent_dict[tenant_name]['VRFs'][vrf_name]['vzAny']['Provided Contracts'].update({provided_contract_name: {}})

        return parent_dict

