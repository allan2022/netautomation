from utils.gettask import GetTask
from utils.getenv import GetEnv
from utils.getsuffix import GetSuffix
from utils.getcredentials import GetCredentials
from utils.filetools import full_load_yaml


class ValidationConfig(GetEnv, GetSuffix, GetCredentials):

    def __init__(self, yaml_file_name, network_env=None):
        super().__init__()
        self.cfg = {}
        self.output_directory = ''
        self.folder_keyword = ''
        self.env_list = []
        self.task = ''
        self.task_list = []
        self.network_env = network_env
        self.get_config(yaml_file_name)


    def get_config(self, yaml_file_name):
        self.cfg = full_load_yaml(yaml_file_name)

        if not self.cfg:
            print()
            print(f'{yaml_file_name} not found! Exit the program!')
            print()
            exit()

        tasks = self.cfg.get('tasks')
        if tasks:
            self.task_list = tasks.split()
            gettask = GetTask(self.task_list)
            gettask.get_task()
            self.task = gettask.task
            if self.network_env:
                if self.task.startswith('baseline_check') or self.task.startswith('post_check'):
                    self.folder_keyword = self.task.split('_')[0]
                    if 'aci' in self.network_env:
                        env_list = [*self.cfg['aci_fabrics'].keys()]
                        self.get_env(env_list)
                        env_cfg = self.cfg['aci_fabrics'].get(f"{self.env}", {})
                        self.get_ip_username_password(env_cfg, 'aci')
                    if 'core' in self.network_env:
                        env_list = [*self.cfg['core_networks'].keys()]
                        self.get_env(env_list)
                        env_cfg = self.cfg['core_networks'].get(f"{self.env}", {})
                        self.get_ip_username_password(env_cfg, 'core')
                    original_folder_suffix = self.cfg.get('result_folder_suffix')
                    self.get_suffix(original_folder_suffix)
                else:
                    return
        else:
            print()
            print(f'No "tasks" configured in {yaml_file_name}! Exit the program!')
            print()
            quit()
