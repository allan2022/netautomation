from validationtools.validationquery import ValidationQuery
from endpointtracker.endpointtable import EndpointTable
from endpointtracker.endpointjson import EndpointJson
from utils.filetools import create_folder, get_lastest_folder


class EndpointTracker(ValidationQuery):

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.query_data(self.config)
        self.latest_baseline_folder = get_lastest_folder(f"{self.config.cfg['output_directory']}/baseline_check", f'{self.config.env} aci', exit=True)

        self.endpoint_tracker_directory = f"{self.config.cfg['output_directory']}/aci_endpoint_tracker/{self.config.env}"
        create_folder(self.endpoint_tracker_directory)
        endpoint_tracker_table = EndpointTable(self)
        endpoint_tracker_table.build_endpoint_tracker_table(self)
        endpoint_tracker_json = EndpointJson()
        endpoint_tracker_json.build_endpoint_tracker_json(self)
