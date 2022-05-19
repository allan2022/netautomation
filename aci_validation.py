import os
from utils.get_task import get_task
from envtools.setup_environment import SetupEnvironment
from acitools.aci_auth import aci_auth
import acitools.aci_collect_info

CORE_ENVIRONMENT = os.getcwd() + '/src/core_environment.yaml'

class ACIValidation:
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

    def aci_validation(self):
        
        if self.task_select != None and self.aci_select != None:
            aci_env = SetupEnvironment(CORE_ENVIRONMENT)

            if aci_env.change_number != "":
                aci_env.setup_validation_aci(CORE_ENVIRONMENT, self.task_select, self.aci_select)

                base_url = aci_env.base_url
                auth_url = aci_env.auth_url
                auth_data = aci_env.auth_data
                snapshot_folder = aci_env.snapshot_folder          

                session = aci_auth(auth_url, auth_data)

                print(session)
                # aci_info = acitools.aci_collect_info.collect()












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
    av = ACIValidation()
    av.aci_validation()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n tast aborted")