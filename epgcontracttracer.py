from os import getcwd
from utils.selectitem import SelectItem
from utils.generalconfigandtask import GeneralConfigAndTask
from utils.getcredentials import GetCredentials
from endpointtracer.realtimetracer import RealtimeTracer


EPG_CONTRACT_TRACER_CONFIG = getcwd() + '/src/epg_contract_tracer_config.yaml'


class EpgContractTracerMain(GeneralConfigAndTask, GetCredentials):

    def __init__(self):
        GeneralConfigAndTask.__init__(self, EPG_CONTRACT_TRACER_CONFIG)
        GetCredentials.__init__(self)
        #inherit self.cfg, self.task, self.select_item, self.username, self.password, self.address, get_ip_username_password
        self.task_list = ['realtime_tracer', 'baseline_tracer']
        self.task = 'realtime_tracer'
        self.vrf_list = ['BLUE', 'GREEN', 'RED']


    def epg_contract_tracer_main(self):
        env_list = list(self.cfg['aci_fabrics'].keys())
        self.env = self.select_item(env_list, 'Select an ACI Fabric')
        self.get_ip_username_password(self.cfg['aci_fabrics'][self.env], 'aci')
        self.vrf = self.select_item(self.vrf_list, 'Select VRF')
        # self.task = self.select_item(self.task_list, 'Select a task')

        if self.task == 'realtime_tracer':
            realtime_tracer = RealtimeTracer(self)
            realtime_tracer.realtime_tracer()


def main():
    epg_contract_tracer = EpgContractTracerMain()
    epg_contract_tracer.epg_contract_tracer_main()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
