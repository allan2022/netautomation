import requests
import json
  
def collect_all_vlanpools(session, base_url):        
    vlanpools_list = []
    vlanpools_json = {}
    total_count = 0

    vlanpool_class = 'node/class/fvnsVlanInstP.json?'
    vlanpool_url = base_url + vlanpool_class

    vlanpools = session.get(vlanpool_url, verify=False)

    vlanpools_json = vlanpools.json()
    total_count = int(vlanpools_json["totalCount"])

    try:
        index = 0
        vlanpools_list.clear()
        for i in range(0, total_count):
            vlanpools_list.append(vlanpools_json["imdata"][index]["fvTenant"]["attributes"]["name"])
            index = index + 1
    except IndexError:
        pass

    return vlanpools_list, vlanpools_json
