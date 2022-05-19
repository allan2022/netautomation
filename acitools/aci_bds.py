import requests
import json
  
def collect_all_bds(session, base_url):        
    bds_list = []
    bds_json = {}
    total_count = 0

    bd_class = 'node/class/fvBD.json?'
    bd_url = base_url + bd_class

    bds = session.get(bd_url, verify=False)

    bds_json = bds.json()
    total_count = int(bds_json["totalCount"])

    try:
        index = 0
        bds_list.clear()
        for i in range(0, total_count):
            bds_list.append(bds_json["imdata"][index]["fvBD"]["attributes"]["name"])
            index = index + 1
    except IndexError:
        pass

    return bds_list, bds_json

