import requests
import json
  
def collect_all_vrfs(session, base_url):        
    vrfs_list = []
    vrfs_json = {}
    total_count = 0

    vrf_class = 'node/class/fvCtx.json?'
    vrf_url = base_url + vrf_class

    vrfs = session.get(vrf_url, verify=False)

    vrfs_json = vrfs.json()
    total_count = int(vrfs_json["totalCount"])

    try:
        index = 0
        vrfs_list.clear()
        for i in range(0, total_count):
            vrfs_list.append(vrfs_json["imdata"][index]["fvCtx"]["attributes"]["name"])
            index = index + 1
    except IndexError:
        pass

    return vrfs_list, vrfs_json

