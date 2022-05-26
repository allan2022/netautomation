from email.charset import add_charset
import requests
import json
  
class ACITenants:

    def __init__(self):
        self.tenants_list = []
        self.tenants_json = {}
        self.tenant = None

    def collect_all_tenants(self, session, base_url):        
        total_count = 0

        tenant_class = 'node/class/fvTenant.json?'
        tenant_url = base_url + tenant_class

        tenants = session.get(tenant_url, verify=False)

        self.tenants_json = tenants.json()
        total_count = int(self.tenants_json["totalCount"])

        try:
            index = 0
            self.tenants_list.clear()
            for i in range(0, total_count):
                self.tenants_list.append(self.tenants_json["imdata"][index]["fvTenant"]["attributes"]["name"])
                index = index + 1
        except IndexError:
            pass

        return self.tenants_list, self.tenants_json

    def add_tenant (self, session, base_url, tenant):
        self.collect_all_tenants(session, base_url)

        add_res = None
        url = base_url + "/mo/uni.json"

        if tenant not in self.tenants_list:
            data = {
                "fvTenant":{
                    "attributes":{
                        "dn": f"uni/tn-{tenant}",
                        "status": "created"
                    }
                }
            }

            try:
                add_res = session.post(url, json=data, verify=False)
            except:
                print(f'add tenant {tenant} failed')

        else:
            print("tenant already exists.")

        return add_res

    def del_tenant (self, session, base_url, tenant):
        self.collect_all_tenants(session, base_url)

        del_res = None
        url = base_url + "/mo/uni.json"

        if tenant in self.tenants_list:
            data = {
                "fvTenant":{
                    "attributes":{
                        "dn": f"/uni/tn-{tenant}",
                        "status": "deleted"
                    }
                }
            }

            try:
                del_res = session.post(url, json=data, verify=False)
            except:
                print(f'delete tenant {tenant} failed.')

        else:
            print("tenant does not exist.")

        return del_res

    def search_tenant (self, session, base_url, tenant):
        self.collect_all_tenants(session, base_url)

        search_res = None
        url = base_url + f"/node/mo/uni/tn-{tenant}.json"

        if tenant in self.tenants_list:
            search_res = session.get(url, verify=False)

        return search_res