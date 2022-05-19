import requests
import json
  
def collect_all_epgs(session, base_url):        
    tenants_list = []
    tenants_json = {}
    total_count = 0

    tenant_class = 'node/class/fvTenant.json?'
    tenant_url = base_url + tenant_class

    tenants = session.get(tenant_url, verify=False)

    print(type(tenants))
    print(tenants)
    # self.tenants_json = tenants.json()
    # self.total_count = int(self.tenants_json["totalCount"])

    try:
        index = 0
        tenants_list.clear()
        for i in range(0, total_count):
            tenants_list.append(tenants_json["imdata"][index]["fvTenant"]["attributes"]["name"])
            index = index + 1
    except IndexError:
        pass
    return tenants_list, tenants_json

