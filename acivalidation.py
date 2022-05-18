import datetime
from os import getcwd
from validationtools.validationconfig import ValidationConfig
from validationtools.validationcheck import ValidationCheck
from endpointtracker.endpointtrackerconfig import EndpointTrackerConfig
from endpointtracker.endpointtracker import EndpointTracker
from endpointtracer.endpointtracerconfig import EndpointTracerConfig
from endpointtracer.endpointtracer import EndpointTracer
from redgreenplan.changeplan import ChangePlan
from pyatstools.pyatsdiff import PyatsDiff
from aciapitools.generalquery import GeneralQuery
from utils.filetools import rename_folder_with_suffix


ACI_VALIDATION_CONFIG = getcwd() + '/src/aci_validation_config.yaml'


class AciValidation():
    def __init__(self):
        self.config = ValidationConfig(ACI_VALIDATION_CONFIG, 'aci')


    def aci_validation(self):
        if self.config.task == 'WP_change_plan_creation':
            ChangePlan(self.config, 'wp')
        elif self.config.task == 'WS_change_plan_validation':
            ChangePlan(self.config, 'ws')
        elif self.config.task == 'change_plan_diff':
            PyatsDiff(parent_class=self.config, keyword=self.config.task)
        elif self.config.task == 'update_endpoint_tracker':
            epconfig = EndpointTrackerConfig(ACI_VALIDATION_CONFIG)
            eptracker = EndpointTracker(epconfig)
        elif self.config.task == 'endpoint_epg_contract_tracer':
            epconfig = EndpointTracerConfig(ACI_VALIDATION_CONFIG)
            eptracer = EndpointTracer(epconfig)
        elif self.config.task == 'query_api_by_url_class_dn':
            queryaci = GeneralQuery(ACI_VALIDATION_CONFIG, self.config.task)
            queryaci.general_query()
        else:
            start =  datetime.datetime.now()
            apic = ValidationCheck(self.config)
            apic.output_directory = rename_folder_with_suffix(apic.output_directory, self.config.folder_suffix)
            if self.config.task.startswith('post_check'):
                print('PyatsDiff......')
                PyatsDiff(parent_class=apic, keyword='aci')

            end = datetime.datetime.now()
            print('Execution time : ', end - start)
            print()


def main():
    validation = AciValidation()
    validation.aci_validation()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
