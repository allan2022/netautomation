import json


class EndpointJson():

    def __init__(self, ep=None):
        pass


    def build_endpoint_tracker_json(self, ep):
        """
        Create endpoint infofor selected ACI Fabric in JSON format. 
        This is for WS automation script to pick up the file and process the endpoint info
        data.append({"mac":ep.mac, "ip":ep.ip, "tenant":tenant.name, "app":app_profile.name, "epg":epg.name})
        """

        print()
        print('Executing build_endpoint_tracker_json_output()...')
        print()
        endpoint_tracker_file = f'{ep.endpoint_tracker_directory}/{ep.config.env}_endpoints_jsonout.json'
        endpoint_tracker_list = []
        build_endpoint_tracker_sequence_list = ep.config.cfg.get('build_dict_sequence')['build_endpoint_tracker_sequence'].split()
        for build_class in build_endpoint_tracker_sequence_list:
            endpoint_tracker_list = self.build_endpoint_tracker_json_output(endpoint_tracker_list, build_class, ep)
        with open(endpoint_tracker_file, "w") as outfile:
            json.dump(endpoint_tracker_list, outfile)
        print()
        print('-'*150)
        print('endpoint json file name : ', endpoint_tracker_file)
        print('-'*150)
        print()


    def build_endpoint_tracker_json_output(self, parent_list, build_class, ep):
        for item in ep.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']
            if build_class == 'fvCEp':
                epg_vrf_dn = item_dn.split('/cep-')[0]
                ip = item[build_class]['attributes']['ip']
                mac = item[build_class]['attributes']['mac']
                if '/ap-' in epg_vrf_dn and '/epg-' in epg_vrf_dn:
                    tenant = item_dn.split('/tn-')[-1].split('/ap-')[0]
                    app_profile = item_dn.split('/ap-')[-1].split('/epg-')[0]
                    epg = item_dn.split('/epg-')[-1].split('/cep-')[0]
                    parent_list.append({"mac":mac, "ip":ip, "tenant":tenant, "app":app_profile, "epg":epg})

        return parent_list
