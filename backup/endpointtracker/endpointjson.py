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
        endpoint_tracker_list = self.build_endpoint_tracker_json_output(ep)
        with open(endpoint_tracker_file, "w") as outfile:
            json.dump(endpoint_tracker_list, outfile)
        print()
        print('-'*150)
        print('endpoint json file name : ', endpoint_tracker_file)
        print('-'*150)
        print()


    def build_endpoint_tracker_json_output(self, ep):
        df = ep.endpoint_tracker_table
        endpoint_tracker_list = []
        for i in range(len(df)):
            endpoint_dict = {'mac':df['mac'][i], 'ip':df['ip'][i], 'tenant':df['tenant'][i], 'app':df['ap'][i], 'epg':df['epg'][i]}
            endpoint_tracker_list.append(endpoint_dict)
        return endpoint_tracker_list
