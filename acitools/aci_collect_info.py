import requests
import json
import os

class collect():
    def __init__(self):
        pass
    
    def aci_query_obj(self, session, base_url, **kwargs):        
        self.tenant = ""
        self.ap = ""
        self.bd = ""
        self.vrf = ""
        self.epg = ""
        self.subnet = ""
        self.tenant_list = []
        self.tenat_json = {}
        self.ap_list = []
        self.bd_list = []
        self.vrf_list = []
        self.epg_list = []
        self.subnet_list = []
        self.total_count = 0

        for key, value in kwargs.items():
            if key == "tenant":
                self.tenant = value
            elif key == "ap":
                self.ap = value
            elif key == "bd":
                self.bd = value
            elif key == "vrf":
                self.vrf = value
            elif key == "epg":
                self.epg = value
            elif key == "subnet":
                self.subnet == value
            else:
                break 

        # return a list of all tenants
        if self.tenant == "":
            tenant_class = 'node/class/fvTenant.json?'
            tenant_url = base_url + tenant_class

            tenants = session.get(tenant_url, verify=False)
            self.tenants_json = tenants.json()
            self.total_count = int(self.tenants_json["totalCount"])

            try:
                index = 0
                self.tenant_list.clear()
                for i in range(0, self.total_count):
                    self.tenant_list.append(self.tenants_json["imdata"][index]["fvTenant"]["attributes"]["name"])
                    index = index + 1
            except IndexError:
                pass
            return self.tenant_list, self.tenants_json

        # return a list of all application profiles of the specified tenant     
        elif self.ap == "all":
            tenant_mo = 'node/mo/uni/tn-{tenant_name}.json?'.format(tenant_name=self.tenant)
            ap_filter = "query-target=children&target-subtree-class=fvAp"
            ap_url = base_url + tenant_mo + ap_filter

            aps = session.get(ap_url, verify=False)
            aps_json = aps.json()
            self.total_count = int(aps_json["totalCount"])

            try:
                index = 0
                self.ap_list.clear()
                for i in range(0, self.total_count):
                    self.ap_list.append(aps_json["imdata"][index]["fvAp"]["attributes"]["name"])
                    index = index + 1
            except IndexError:
                pass
            return self.ap_list

        # return a list of all bridge domain of the specified tenant
        elif self.bd == "all":
            tenant_mo = 'node/mo/uni/tn-{tenant_name}.json?'.format(tenant_name=self.tenant)
            bd_filter = "query-target=children&target-subtree-class=fvBD"
            bd_url = base_url + tenant_mo + bd_filter

            bds = session.get(bd_url, verify=False)
            bds_json = bds.json()
            self.total_count = int(bds_json["totalCount"])

            try:
                index = 0
                self.bd_list.clear()
                for i in range(0, self.total_count):
                    self.bd_list.append(bds_json["imdata"][index]["fvBD"]["attributes"]["name"])
                    index = index + 1
            except IndexError:
                pass
            return self.bd_list
        
        # return a list of all vrf of the specified tenant
        elif self.vrf ==  "all":
            tenant_mo = 'node/mo/uni/tn-{tenant_name}.json?'.format(tenant_name=self.tenant)
            vrf_filter = "query-target=children&target-subtree-class=fvCtx"
            vrf_url = base_url + tenant_mo + vrf_filter

            vrfs = session.get(vrf_url, verify=False)
            vrfs_json = vrfs.json()
            self.total_count = int(vrfs_json["totalCount"])

            try:
                index = 0
                self.vrf_list.clear()
                for i in range(0, self.total_count):
                    self.vrf_list.append(vrfs_json["imdata"][index]["fvCtx"]["attributes"]["name"])
                    index = index + 1
            except IndexError:
                pass
            return self.vrf_list        
        
        # return a list of all epgs of the specified application profile and tenant
        elif self.epg == "all":
            ap_mo = 'node/mo/uni/tn-{tenant_name}/ap-{ap_name}.json?'.format(tenant_name=self.tenant, ap_name=self.ap)
            epg_filter = "query-target=children&target-subtree-class=fvAEPg"
            epg_url = base_url + ap_mo + epg_filter

            epgs = session.get(epg_url, verify=False)
            epgs_json = epgs.json()
            self.total_count = int(epgs_json["totalCount"])

            try:
                index = 0
                self.epg_list.clear()
                for i in range(0, self.total_count):
                    self.epg_list.append(epgs_json["imdata"][index]["fvAEPg"]["attributes"]["name"])
                    index = index + 1
            except IndexError:
                pass
            return self.epg_list  
        
        elif self.subnet != "":
                pass
        else:
            print("Please provide proper object name.")


class change(collect):
    def __init__(self):
        pass
    
    def aci_create_obj(self, session, base_url, **kwargs):        
        self.tenant_c = ""
        self.ap_c = ""
        self.bd_c = ""
        self.vrf_c = ""
        self.epg_c = ""
        self.subnet_c = ""
        self.tenant_json = {}
        self.ap_json = {}
        self.bd_json = {}
        self.vrf_json = {}
        self.epg_json = {}
        self.subnet_list = {}

        for key, value in kwargs.items():
            if key == "tenant":
                self.tenant_c = value
            elif key == "ap":
                self.ap_c = value
            elif key == "bd":
                self.bd_c = value
            elif key == "vrf":
                self.vrf_c = value
            elif key == "epg":
                self.epg_c = value
            elif key == "subnet":
                self.subnet_c == value
            else:
                break        

        tenants = self.aci_query_obj(session, base_url)

        # create tenants
        if self.tenant_c != "" and self.ap_c == "" and self.bd_c == "" and self.vrf_c == "" and self.epg_c == "" and self.subnet_c == "":

            # tenant exists
            if self.tenant_c in tenants:
                print("Tenant \"{}\" already exists.".format(self.tenant_c))            
            # tenant not exists    
            else:
                tenant_mo = 'node/mo/uni/tn-{}.json'.format(self.tenant_c)
                tenant_url = base_url + tenant_mo               
                payload = {
                    "fvTenant": {
                        "attributes": {
                        "name": "{}".format(self.tenant_c),
                        "status": "created"
                        }
                    }
                }
                tenant = session.post(tenant_url, json=payload, verify=False)
                self.tenant_json = tenant.json()
                
                # add succeeds
                if (tenant.status_code == 200):
                    print("Tenant \"{}\" is created.".format(self.tenant_c))
                # add fails
                else:
                    print("Failed to create tenant \"{}\"".format(self.tenant_c))     
            return self.tenant_json

        # add VRF
        elif self.tenant_c != "" and self.ap_c == "" and self.bd_c == "" and self.vrf_c != "" and self.epg_c == "" and self.subnet_c == "":
            
            # tenant not exists
            if self.tenant_c not in tenants:
                print("Tenant \"{}\" doesn't exist. Define tenant first.".format(self.tenant_c))
            # tenant exists    
            else:
                vrfs = self.aci_query_obj(session, base_url, tenant=self.tenant_c, vrf="all")
                
                # VRF exists
                if self.vrf_c in vrfs:
                    print("VRF \"{}\" already exists.".format(self.vrf_c))
                # VRF not exists
                else:
                    tenant_mo = 'node/mo/uni/tn-{}.json'.format(self.tenant_c)
                    tenant_url = base_url + tenant_mo                    
                    payload = {
                        "fvCtx": {
                            "attributes": {
                            "name": "{}".format(self.vrf_c),
                            "status": "created"
                            }
                        }
                    }
                    vrf = session.post(tenant_url, json=payload, verify=False)
                    self.vrf_json = vrf.json()
                    
                    # add succeeds
                    if (vrf.status_code == 200):
                        print("VRF \"{}\" is created.".format(self.vrf_c))
                    # add fails
                    else:
                        print("Failed to create VRF \"{}\"".format(self.vrf_c))     
            return self.vrf_json

        # add AP
        elif self.tenant_c != "" and self.ap_c != "" and self.bd_c == "" and self.vrf_c == "" and self.epg_c == "" and self.subnet_c == "":
            
            # tenant not exists
            if self.tenant_c not in tenants:
                print("Tenant \"{}\" doesn't exist. Define tenant first.".format(self.tenant_c))
            # tenant exists    
            else:
                aps = self.aci_query_obj(session, base_url, tenant=self.tenant_c, ap="all")
                
                # AP exists
                if self.ap_c in aps:
                    print("AP \"{}\" already exists.".format(self.ap_c))
                # AP not exists
                else:
                    tenant_mo = 'node/mo/uni/tn-{}.json'.format(self.tenant_c)
                    tenant_url = base_url + tenant_mo                    
                    payload = {
                        "fvAp": {
                            "attributes": {
                                "name": "{}".format(self.ap_c),
                                "status": "created"
                            }
                        }
                    }
                    ap = session.post(tenant_url, json=payload, verify=False)
                    self.ap_json = ap.json()
                    
                    # add succeeds
                    if (ap.status_code == 200):
                        print("AP \"{}\" is created.".format(self.ap_c))
                    # add fails
                    else:
                        print("Failed to create AP \"{}\"".format(self.ap_c))     
            return self.ap_json

        # add BD
        elif self.tenant_c != "" and self.ap_c == "" and self.bd_c != "" and self.epg_c == "" and self.subnet_c == "":
            
            # tenant not exists
            if self.tenant_c not in tenants:
                print("Tenant \"{}\" doesn't exist. Define tenant first.".format(self.tenant_c))
            # tenant exists    
            else:
                bds = self.aci_query_obj(session, base_url, tenant=self.tenant_c, bd="all")
                
                # BD exists
                if self.bd_c in bds:
                    print("BD \"{}\" already exists.".format(self.bd_c))
                # BD not exists
                else:
                    tenant_mo = 'node/mo/uni/tn-{}.json'.format(self.tenant_c)
                    tenant_url = base_url + tenant_mo                    
                    payload = { 
                        "fvBD": {
                            "attributes": {
                                "name": "{}".format(self.bd_c),
                                "status": "created"
                            },
                            "children": [
                                {
                                    "fvRsCtx": {
                                        "attributes": {
                                            "tnFvCtxName": "{}".format(self.vrf_c)
                                        }
                                    }
                                }
                            ]
                        }
                    }
                    bd = session.post(tenant_url, json=payload, verify=False)
                    self.bd_json = bd.json()
                    
                    # add succeeds
                    if (bd.status_code == 200):
                        print("BD \"{}\" is created.".format(self.bd_c))
                    # add fails
                    else:
                        print("Failed to create BD \"{}\"".format(self.bd_c))     
            return self.bd_json
    
        # add EPG
        elif self.tenant_c != "" and self.ap_c != "" and self.bd_c == "" and self.vrf_c == "" and self.epg_c != "" and self.subnet_c == "":
            
            # tenant not exists
            if self.tenant_c not in tenants:
                print("Tenant \"{}\" doesn't exist. Define tenant first.".format(self.tenant_c))
            # tenant exists    
            else:                
                aps = self.aci_query_obj(session, base_url, tenant=self.tenant_c, ap="all")
                
                # AP not exists
                if self.ap_c not in aps:
                    print("AP \"{}\" doesn't exists. Define AP first.".format(self.ap_c))
                # AP exists
                else:
                    epgs = self.aci_query_obj(session, base_url, tenant=self.tenant_c, ap=self.ap_c, epg="all")

                    # EPG exists
                    if self.epg_c in epgs:
                        print("EPG \"{}\" already exists.".format(self.epg_c))
                    # EPG not exists
                    else:                    
                        ap_mo = 'node/mo/uni/tn-{}/ap-{}.json'.format(self.tenant_c, self.ap_c)
                        ap_url = base_url + ap_mo                    
                        payload = {
                                "fvAEPg": {
                                    "attributes": {
                                        "name": "{}".format(self.epg_c),
                                        "status": "created"
                                    }
                                }
                        }
                        epg = session.post(ap_url, json=payload, verify=False)
                        self.epg_json = epg.json()
                        
                        # add succeeds
                        if (epg.status_code == 200):
                            print("EPG \"{}\" is created.".format(self.epg_c))
                        # add fails
                        else:
                            print("Failed to create EPG \"{}\"".format(self.epg_c))     
            return self.epg_json
        else:
            print("Please provide proper object name.")


    def aci_delete_obj(self, session, base_url, **kwargs):        
        self.tenant_d_c = ""
        self.ap_d = ""
        self.bd_d = ""
        self.vrf_d = ""
        self.epg_d = ""
        self.subnet_d = ""
        self.tenant_json = {}
        self.ap_json = {}
        self.bd_json = {}
        self.vrf_json = {}
        self.epg_json = {}
        self.subnet_list = {}

        for key, value in kwargs.items():
            if key == "tenant":
                self.tenant_d = value
            elif key == "ap":
                self.ap_d = value
            elif key == "bd":
                self.bd_d = value
            elif key == "vrf":
                self.vrf_d = value
            elif key == "epg":
                self.epg_d = value
            elif key == "subnet":
                self.subnet_d == value
            else:
                break 
                
        # delete tenants
        if self.tenant_d != "" and self.ap_d == "" and self.bd_d == "" and self.vrf_d == "" and self.epg_d == "" and self.subnet_d == "":
            tenants = self.aci_query_obj(session, base_url)  
            
            # tenant not exists
            if self.tenant_d not in tenants:
                print("Tenant \"{}\" doesn't exists.".format(self.tenant_d))            
            # tenant exists    
            else:
                tenant_mo = 'node/mo/uni/tn-{}.json'.format(self.tenant_d)
                tenant_url = base_url + tenant_mo               
                payload = {
                    "fvTenant": {
                        "attributes": {
                        "status": "deleted"
                        }
                    }
                }
                tenant = session.post(tenant_url, json=payload, verify=False)
                self.tenant_json = tenant.json()
                
                # delete succeeds
                if (tenant.status_code == 200):
                    print("Tenant \"{}\" is deleted.".format(self.tenant_d))
                # delete fails
                else:
                    print("Failed to delete tenant \"{}\"".format(self.tenant_d))     
            return self.tenant_json

        # delete VRF
        elif self.tenant_d != "" and self.ap_d == "" and self.bd_d == "" and self.vrf_d != "" and self.epg_d == "" and self.subnet_d == "":
            vrfs = self.aci_query_obj(session, base_url, tenant=self.tenant_d, vrf="all")

            # vrf not exists
            if self.vrf_d not in vrfs:
                print("VRF \"{}\" doesn't exist.".format(self.vrf_d))
            # vrf exists    
            else:
                tenant_mo = 'node/mo/uni/tn-{}.json'.format(self.tenant_d)
                tenant_url = base_url + tenant_mo     
                payload = {
                    "fvCtx": {
                        "attributes": {
                            "name": "{}".format(self.vrf_d),
                            "status": "deleted"    
                        }
                    }
                }
                vrf = session.post(tenant_url, json=payload, verify=False)
                self.vrf_json = vrf.json()
                
                # add succeeds
                if (vrf.status_code == 200):
                    print("VRF \"{}\" is deleted.".format(self.vrf_d))
                # add fails
                else:
                    print("Failed to delete VRF \"{}\"".format(self.vrf_d))     
            return self.vrf_json

        # delete AP
        elif self.tenant_d != "" and self.ap_d != "" and self.bd_d == "" and self.vrf_d == "" and self.epg_d == "" and self.subnet_d == "":
            aps = self.aci_query_obj(session, base_url, tenant=self.tenant_d, ap="all")

            # AP not exists
            if self.ap_d not in aps:
                print("AP \"{}\" doesn't exist.".format(self.ap_d))
            # AP exists    
            else:              
                tenant_mo = 'node/mo/uni/tn-{}.json'.format(self.tenant_d)
                tenant_url = base_url + tenant_mo                    
                payload = {
                    "fvAp": {
                        "attributes": {
                            "name": "{}".format(self.ap_d),
                            "status": "deleted"
                        }
                    }
                }
                ap = session.post(tenant_url, json=payload, verify=False)
                self.ap_json = ap.json()
                
                # delete succeeds
                if (ap.status_code == 200):
                    print("AP \"{}\" is deleted.".format(self.ap_d))
                # delete fails
                else:
                    print("Failed to delete AP \"{}\"".format(self.ap_d))     
            return self.ap_json

        # delete BD
        elif self.tenant_d != "" and self.ap_d == "" and self.bd_d != "" and self.vrf_d == "" and self.epg_d == "" and self.subnet_d == "":
            bds = self.aci_query_obj(session, base_url, tenant=self.tenant_d, bd="all")

            # BD not exists
            if self.bd_d not in bds:
                print("BD \"{}\" doesn't exist.".format(self.bd_d))
            # BD exists    
            else:
                tenant_mo = 'node/mo/uni/tn-{}.json'.format(self.tenant_d)
                tenant_url = base_url + tenant_mo                    
                payload = { 
                    "fvBD": {
                        "attributes": {
                        "name": "{}".format(self.bd_d),
                        "status": "deleted"
                        }
                    }
                }
                bd = session.post(tenant_url, json=payload, verify=False)
                self.bd_json = bd.json()
                    
                # add succeeds
                if (bd.status_code == 200):
                    print("BD \"{}\" is deleted.".format(self.bd_d))
                # add fails
                else:
                    print("Failed to delete BD \"{}\"".format(self.bd_d))     
            return self.bd_json
    
        # delete EPG
        elif self.tenant_d != "" and self.ap_d != "" and self.bd_d == "" and self.vrf_d == "" and self.epg_d != "" and self.subnet_d == "":
            epgs = self.aci_query_obj(session, base_url, tenant=self.tenant_d, ap=self.ap_d, epg="all")

            # tenant not exists
            if self.epg_d not in epgs:
                print("EPG \"{}\" doesn't exist.".format(self.tenant_d))
            # tenant exists    
            else:                
                ap_mo = 'node/mo/uni/tn-{}/ap-{}.json'.format(self.tenant_d, self.ap_d)
                ap_url = base_url + ap_mo                    
                payload = {
                        "fvAEPg": {
                            "attributes": {
                                "name": "{}".format(self.epg_d),
                                "status": "deleted"
                            }
                        }
                }
                epg = session.post(ap_url, json=payload, verify=False)
                self.epg_json = epg.json()
                
                # delete succeeds
                if (epg.status_code == 200):
                    print("EPG \"{}\" is deleted.".format(self.epg_d))
                # delete fails
                else:
                    print("Failed to delete EPG \"{}\"".format(self.epg_d))     
            return self.epg_json
        else:
            print("Please provide proper object name.")