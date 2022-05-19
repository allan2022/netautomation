from utils.getenv import GetEnv
from utils.getcredentials import GetCredentials
from utils.filetools import full_load_yaml


class EndpointTrackerConfig(GetEnv, GetCredentials):

    def __init__(self, yaml_file_name):
        super().__init__()
        self.cfg = {}
        self.task = 'endpoint_tracker'
        self.get_aci_config(yaml_file_name)


    def get_aci_config(self, yaml_file_name):
        self.cfg = full_load_yaml(yaml_file_name)

        if not self.cfg:
            print()
            print(f'{yaml_file_name} not found! Exit the program!')
            print()
            exit()

        env_list = [*self.cfg['aci_fabrics'].keys()]
        self.get_env(env_list)
        env_cfg = self.cfg['aci_fabrics'].get(f"{self.env}", {})
        self.get_ip_username_password(env_cfg, 'aci')
        return

