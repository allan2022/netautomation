import os
from utils.get_task import get_task
from envtools.setup_environment import SetupEnvironment
from acitools.aci_auth import aci_auth
import acitools.aci_collect_info

CORE_ENVIRONMENT = os.getcwd() + '/src/core_environment.yaml'

class ACISearch:
    def __init__(self):
        self.task_list = []
        self.aci_list = []
        self.task_select = ""
        self.aci_select = ""   

        try:
            self.task_list, self.task_select = get_task(CORE_ENVIRONMENT, 'sub_tasks')
        except KeyboardInterrupt:
            pass

        if self.task_select == None:
            print("\ntask not available")

        try:
            self.aci_list, self.aci_select = get_task(CORE_ENVIRONMENT, 'aci_list')
        except KeyboardInterrupt:
            pass

        if self.aci_select == None:
            print("\nACI not found")   

    def aci_search(self):
        
        if self.task_select != None and self.aci_select != None:
            aci_env = SetupEnvironment(CORE_ENVIRONMENT)

            if aci_env.change_number != "":
                aci_env.setup_validation_aci(CORE_ENVIRONMENT, self.task_select, self.aci_select)

                base_url = aci_env.base_url
                auth_url = aci_env.auth_url
                auth_data = aci_env.auth_data
                # snapshot_folder = aci_env.snapshot_folder          

                session, res = aci_auth(auth_url, auth_data)

                if res != "Login failed":                
                    aci_info = acitools.aci_collect_info.collect()

                    while True:
                        print("""
                            1. list all tenants
                            2. list all vrf of a tenant
                            3. list all bridge domain of a tenant
                            4. list all applicaiton profiles of a tenant
                            5. list all EPGs of an applicaiton profile
                            6. find tenant
                            7. find vrf
                            8. find bridge domain
                            9. find application profile
                            10. find EPG 
                            11. exit (or ctrl+C)
                            """)
                        task = input("Select task: ")
                        
                        # list all tenants
                        if task == "1":
                            tenants = aci_info.aci_query_obj(session, base_url)
                            for item in tenants:
                                print(item)
                            print("Total {number} Tenants.".format(number=str(len(tenants))))    
                        
                        # list all VRF of a tenant
                        elif task == "2":
                            tenant = input("Enter tenant name: ")
                            vrfs = aci_info.aci_query_obj(session, base_url, tenant=tenant, vrf="all")
                            for item in vrfs:
                                print(item)   
                            print("Total {number} VRFs.".format(number=str(len(vrfs))))                  
                        
                        # list all BD of a tenant
                        elif task == "3":
                            tenant = input("Enter tenant name: ")
                            bds = aci_info.aci_query_obj(session, base_url, tenant=tenant, bd="all")
                            for item in bds:
                                print(item)       
                            print("Total {number} BDs.".format(number=str(len(bds))))            
                        
                        # list all AP of a tenant
                        elif task == "4":
                            tenant = input("Enter tenant name: ")
                            aps = aci_info.aci_query_obj(session, base_url, tenant=tenant, ap="all")
                            for item in aps:
                                print(item)   
                            print("Total {number} APs.".format(number=str(len(aps))))            
                        
                        # list all EPG of a AP
                        elif task == "5":
                            tenant = input("Enter tenant name: ")
                            ap = input("Enter ap name: ")
                            epgs = aci_info.aci_query_obj(session, base_url, tenant=tenant, ap=ap, epg="all")
                            for item in epgs:
                                print(item) 
                            print("Total {number} EPGs.".format(number=str(len(epgs))))              

                        # find tenant   
                        elif task == "6":
                            tenant = input("Enter tenant name: ")
                            tenants = aci_info.aci_query_obj(session, base_url)
                            if tenant in tenants:
                                print("\nTenant \"{tenant}\" is found".format(tenant=tenant))
                            else:
                                print("\nTenant \"{tenant}\" is not found".format(tenant=tenant))
                    
                        # find VRF   
                        elif task == "7":
                            tenant = input("Enter tenant name: ")
                            vrf = input("Enter VRF name: ")
                            vrfs = aci_info.aci_query_obj(session, base_url, tenant=tenant, vrf="all")
                            if vrf in vrfs:
                                print("\nVRF \"{vrf}\" is found".format(vrf=vrf))
                            else:
                                print("\nVRF \"{vrf}\" is not found".format(vrf=vrf))

                        # find BD   
                        elif task == "8":
                            tenant = input("Enter tenant name: ")
                            bd = input("Enter BD name: ")
                            bds = aci_info.aci_query_obj(session, base_url, tenant=tenant, bd="all")
                            if bd in bds:
                                print("\nBD \"{bd}\" is found".format(bd=bd))
                            else:
                                print("\nBD \"{bd}\" is not found".format(bd=bd))

                        # find AP   
                        elif task == "9":
                            tenant = input("Enter tenant name: ")
                            ap = input("Enter AP name: ")
                            aps = aci_info.aci_query_obj(session, base_url, tenant=tenant, ap="all")
                            if bd in bds:
                                print("\nAP \"{ap}\" is found".format(ap=ap))
                            else:
                                print("\nAP \"{ap}\" is not found".format(ap=ap))

                        # find EPG   
                        elif task == "10":
                            tenant = input("Enter tenant name: ")
                            ap = input("Enter AP name: ")
                            epg = input("Enter EPG name: ")
                            epgs = aci_info.aci_query_obj(session, base_url, tenant=tenant, ap=ap, epg="all")
                            if epg in epgs:
                                print("\nEPG \"{epg}\" is found".format(epg=epg))
                            else:
                                print("\nAP \"{epg}\" is not found".format(epg=epg))

                        elif task == "11":
                            break
                        else:
                            print("\nNot a valid choice. Try again")

                        input("\nEnter to continue...")   

                    # if self.task_select == "postchange_snapshot_and_diff_prechange_snapshot":
                    #     print("#####################  compare postchange with prechange #########################")
                    #     before_folder = os.path.join(change_folder, 'prechange_snapshot_0')
                    #     os.system(f'pyats diff {before_folder} {snapshot_folder} --output {change_folder}/diff_dir')
                    
                    # elif self.task_select == "postchange_snapshot_and_diff_last_postchange_snapshot":
                    #     print("#####################  compare postchange with last postchange #########################")
                    #     i = int(snapshot_folder.rsplit('_', 1)[-1]) - 1
                    #     before_folder = os.path.join(change_folder, ('postchange_snapshot_' + str(i)))
                    #     os.system(f'pyats diff {before_folder} {snapshot_folder} --output {change_folder}/diff_dir')
                    
                    # else:
                    #     pass    

def main():
    av = ACISearch()
    av.aci_search()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n tast aborted")