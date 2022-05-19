import requests
import json
  
def collect_all_epgs(self, session, base_url):        
    self.tenant_list = []
    self.tenat_json = {}
    self.total_count = 0

    tenant_class = 'node/class/fvTenant.json?'
    tenant_url = base_url + tenant_class

    tenants = session.get(tenant_url, verify=False)

    print(type(tenants))
    print(tenants)
    # self.tenants_json = tenants.json()
    # self.total_count = int(self.tenants_json["totalCount"])

    try:
        index = 0
        self.tenant_list.clear()
        for i in range(0, self.total_count):
            self.tenant_list.append(self.tenants_json["imdata"][index]["fvTenant"]["attributes"]["name"])
            index = index + 1
    except IndexError:
        pass
    return self.tenant_list, self.tenants_json

