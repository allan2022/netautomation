from validationtools.validationquery import ValidationQuery
from validationtools.vlanpool import VlanPool


class ValidationCheck(ValidationQuery):

    def __init__(self, config):
        super().__init__()
        
        self.config = config
        self.task = config.task
        self.output_directory = self.query_data(self.config)

        self.vlan_pool = VlanPool(self)
        self.vlan_pool.build_vlan_pool_dict(self)

