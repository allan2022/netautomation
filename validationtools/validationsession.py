import os
import requests
import json
from utils.timestamp import Timestamp
from utils.filetools import create_folder


class ValidationSession(Timestamp):

    def __init__(self):
        
        super().__init__()
        self.token = None
        self.headers = {'content-type': "application/json", 'cache-control': "no-cache"}
        self.session = requests.Session()


    def connect(self, config):
        error_msg = ''
        login_url = f"{config.base_url}/api/aaaLogin.json"
        payload = {'aaaUser': {'attributes': {'name': config.username, 'pwd': config.password}}}
        requests.packages.urllib3.disable_warnings()
        response = requests.post(login_url,data=json.dumps(payload), headers=self.headers, verify=False).json()

        if int(response['totalCount']) > 0:
            self.token = response['imdata'][0]['aaaLogin']['attributes']['token']
            print()
            print(f'Successfully login APIC {config.address}')
            print()
            self.get_timestamp()
            if config.task == 'endpoint_tracker' or config.task == 'endpoint_tracer':
                return
            else:
                if 'aci' in config.env:
                    new_output_directory = f"{config.cfg['output_directory']}/{config.folder_keyword}_check/{config.env}_{config.folder_keyword}_{self.timestamp}"
                else:
                    new_output_directory = f"{config.cfg['output_directory']}/{config.folder_keyword}_check/{config.env}_aci_{config.folder_keyword}_{self.timestamp}"
                create_folder(new_output_directory)
                return new_output_directory
        else:
            error_msg = f'failed to connect to APIC {self.address}, Error Code {response.status_code}'
            print(error_msg)
            print()
            quit()
