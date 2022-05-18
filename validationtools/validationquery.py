import re
from validationtools.validationsession import ValidationSession
from utils.aciutils import api_get
from utils.filetools import write_file


class ValidationQuery(ValidationSession):

    def __init__(self):
        ValidationSession.__init__(self)
        self.query_class_no_children_list = []
        self.query_class_with_children_list = []
        self.query_special_url_list = []
        self.query_special_url_dict = {}
        self.data_dict = {}
        self.query_url_response_total_dict = {}
        self.tenant_vrf_name_list = []
        self.tenant_vrf_combined_name_list = []
        self.non_loop_query_class_list = []
        self.loop_query_class_list = []
        self.query_loop_per_tenant_vrf_dn_list = []
        self.query_loop_per_tenant_vrf_name_list = []
        self.query_loop_per_pod_node_list = []
        self.pod_node_combined_name_list = []
        self.response_json = ''


    def query_data(self, config, query_url=None):
        if config.task == 'endpoint_tracer':
            self.connect(config)
            self.query_apic(query_url=query_url, config=None)
            return
        elif config.task == 'endpoint_tracker':
            self.connect(config)
            self.categorize_query_class(config.cfg['aci_query_classes']['endpoint_tracker_query'])
            self.query_apic(config=config)
            return
        else:
            new_output_directory = self.connect(config)
            self.categorize_query_class(config.cfg['aci_query_classes']['validation_query'])
            self.query_apic(config=config, folder=new_output_directory)
            return new_output_directory
        


    def categorize_query_class(self, query):
        for key, value in query.items():
            if isinstance(value, str):
                if key == 'query_class_no_children':
                    self.query_class_no_children_list = value.split()
                if key == 'query_class_with_children':
                    self.query_class_with_children_list = value.split()
                if key == 'query_loop_per_pod_node':
                    self.query_loop_per_pod_node_list = value.split()
                if key == 'query_loop_per_tenant_vrf_dn':
                    self.query_loop_per_tenant_vrf_dn_list = value.split()
                if key == 'query_loop_per_tenant_vrf_name':
                    self.query_loop_per_tenant_vrf_name_list = value.split()
            if isinstance(value, dict):
                if key == 'query_special_urls':
                    self.query_special_url_list = [*value.keys()]
                    self.query_special_url_dict = value
        self.non_loop_query_class_list = self.query_class_no_children_list + self.query_class_with_children_list + self.query_special_url_list
        self.loop_query_class_list = self.query_loop_per_pod_node_list + self.query_loop_per_tenant_vrf_dn_list + self.query_loop_per_tenant_vrf_name_list
        return


    def query_apic(self, config=None, folder=None, query_url=None):
        if config:
            for query_class in self.non_loop_query_class_list:
                if query_class in self.query_class_no_children_list:
                    url = f"{config.base_url}/api/node/class/{query_class}.json"
                if query_class in self.query_class_with_children_list:
                    url = f"{config.base_url}/api/node/class/{query_class}.json?rsp-subtree=children"
                if query_class in self.query_special_url_list:
                    url = f"{config.base_url}/{self.query_special_url_dict[query_class]}"
                self.query_api_and_add_data(url, config=config,  query_class=query_class, loop=None, item_name1=None, item_name2=None)
                if query_class == 'fvCtx':
                    for item in self.data_dict['fvCtx_data']:
                        tenant_vrf_dn = item[query_class]['attributes']['dn']
                        tenant_vrf_combined_name = tenant_vrf_dn.replace('uni/', '')
                        vrf_name = tenant_vrf_dn.split('/ctx-')[-1]
                        tenant_name = tenant_vrf_dn.split('/tn-')[-1].split('/')[0]
                        self.tenant_vrf_name_list.append(f'{tenant_name}:{vrf_name}')
                        self.tenant_vrf_combined_name_list.append(tenant_vrf_combined_name)

            for query_class in self.loop_query_class_list:
                self.data_dict[f'{query_class}_total'] = 0
                if query_class in self.query_loop_per_pod_node_list:
                    for pod_node_combined_name in self.pod_node_combined_name_list:
                        url = f"{config.base_url}/api/node/class/topology/{pod_node_combined_name}/{query_class}.json"
                        self.query_api_and_add_data(url, config=config,  query_class=query_class, loop=True, item_name1=pod_node_combined_name, item_name2=None)
                if query_class in self.query_loop_per_tenant_vrf_dn_list:
                    for tenant_vrf_combined_name in self.tenant_vrf_combined_name_list:
                        url = f"{config.base_url}/api/node/mo/uni/{tenant_vrf_combined_name}/{query_class}.json?rsp-subtree=children"
                        self.query_api_and_add_data(url, config=config,  query_class=query_class, loop=True, item_name1=tenant_vrf_combined_name, item_name2=None)
                if query_class in self.query_loop_per_tenant_vrf_name_list:
                    for tenant_vrf_name in self.tenant_vrf_name_list:
                        if query_class == 'uribv4Route':
                            url = f'{config.base_url}/api/class/uribv4Route.json?query-target-filter=wcard(uribv4Route.dn,"{tenant_vrf_name}")&rsp-subtree=full&order-by=uribv4Route.dn|asc'
                        self.query_api_and_add_data(url, config=config,  query_class=query_class, loop=True, item_name1=tenant_vrf_name, item_name2=None)
                self.query_url_response_total_dict[f"{query_class} all"] = {'totalCount': self.data_dict[f'{query_class}_total']}
            if folder:
                write_file(f'{folder}/Query_URLs_and_total_counts_parsed.txt', self.query_url_response_total_dict)

        if query_url:
            self.query_api_and_add_data(query_url)


    def query_api_and_add_data(self, url, config=None, query_class=None, loop=None, item_name1=None, item_name2=None):
        print()
        print('GET : ', url)
        response_json = api_get(self.token, url)
        response_total = response_json.get('totalCount')
        if response_total:
            print('Total entries : ', response_total)
        else:
            print(response_json)

        if config:
            query_and_exit_keyword = config.cfg['aci_query_classes'].get('query_and_exit_keyword')
            file_keyword_list = query_and_exit_keyword.replace(':', '_').split()
            file_keyword = '_'.join(file_keyword_list)
            search_result = []
            if query_and_exit_keyword and 'none' not in query_and_exit_keyword.lower():
                query_and_exit_keyword_list = query_and_exit_keyword.split()
                for keyword in query_and_exit_keyword_list:
                    search_result.append(re.search(keyword, url))
                if None not in search_result:
                    write_file(f'/data/netdevops/verification/baseline_check/{config.env}_{file_keyword}_raw_json.txt', response_json)
                    exit()
            if response_total and query_class:
                self.query_url_response_total_dict[url] = {'totalCount': int(response_total)}
                if query_class:
                    if not item_name1 and not item_name2:
                        self.data_dict[f'{query_class}_data'] = response_json['imdata']
                        self.data_dict[f'{query_class}_total'] = int(response_total)
                    if item_name1 and not item_name2:
                        self.data_dict[f'{query_class}_{item_name1}_data'] = response_json['imdata']
                        self.data_dict[f'{query_class}_{item_name1}_total'] = int(response_total)
                    if not item_name1 and item_name2:
                        self.data_dict[f'{query_class}_{item_name2}_data'] = response_json['imdata']
                        self.data_dict[f'{query_class}_{item_name2}_total'] = int(response_total)
                    if item_name1 and item_name2:
                        self.data_dict[f'{query_class}_{item_name1}_{item_name2}_data'] = response_json['imdata']
                        self.data_dict[f'{query_class}_{item_name1}_{item_name2}_total'] = int(response_total)
                    if loop:
                        self.data_dict[f'{query_class}_total'] += int(response_total)
        else:
            self.response_json = response_json
        return

        

