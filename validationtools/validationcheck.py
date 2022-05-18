from validationtools.validationquery import ValidationQuery
from validationtools.epgbd import EpgBd
# from validationtools.addendpoint import AddEndpoint
from validationtools.contractfilter import ContractFilter
from validationtools.bgppeer import BgpPeer
from validationtools.fabricinterface import FabricInterface
from validationtools.fabricnode import FabricNode
from validationtools.lldpneighbor import LldpNeighbor
from validationtools.vpcinterface import VpcInterface
from validationtools.epgvpc import EpgVpc
from validationtools.ospfneighbor import OspfNeighbor
from validationtools.vlanpool import VlanPool
from validationtools.vrfroute import VrfRoute
from validationtools.epgbase import EpgBase
from validationtools.consumercontract import ConsumerContract
from validationtools.providercontract import ProviderContract
from validationtools.epgcontract import EpgContract
from validationtools.externalsubnet import ExternalSubnet
from validationtools.vzany import VzAny
from validationtools.staticroutes import StaticRoutes
from validationtools.subjectfilterentry import SubjectFilterEntry
from validationtools.endpointdict import EndpointDict
from validationtools.bridgedomain import BridgeDomain
from validationtools.l3outvrf import L3outVrf
from validationtools.l3outdict import L3outDict
from validationtools.applicationepg import ApplicationEpg
from validationtools.externalepg import ExternalEpg
from validationtools.contractepg import ContractEpg
from validationtools.vrfinternalsubnet import VrfInternalSubnet
# from validationtools.concreterule import ConcreteRule
from validationtools.topsystem import TopSystem
from validationtools.checkconfigsnapshot import CheckConfigSnapshot
from utils.filetools import write_file
from collections import defaultdict
from copy import deepcopy


class ValidationCheck(ValidationQuery):

    def __init__(self, config):
        super().__init__()
        
        self.config = config
        self.task = config.task
        self.output_directory = self.query_data(self.config)
        self.scope_vrf_dict = {"16777200": "black-hole"}
        self.vrf_scope_dict = {"black-hole": "16777200"}
        self.tenant_networking_epg_dict = defaultdict(dict)
        self.green_vrf_endpoints_dict = {}
        self.red_vrf_endpoints_dict = {}
        self.blue_vrf_endpoints_dict = {}
        self.Fabric_Extension_Connection_dict = {}
        self.l3out_interface_mapping_dict = {}
        
        self.appcentric_vrf_validation = config.cfg.get('appcentric_vrf_validation')
        self.appcentric_vrf_list = config.cfg.get('appcentric_vrf_list').split()
        self.vrf = ''
        self.epg_bd_subnet_dict = defaultdict(dict)
        self.internal_subnet_to_bd_mapping_dict = {}
        self.internal_subnet_to_epg_mapping_dict = {}
        self.external_subnet_to_epg_mapping_dict = {}
        self.external_subnet_to_epg_per_vrf_mapping_dict = {}
        self.contract_filter_dict = defaultdict(dict)
        self.epg_vrf_mapping_dict = {}
        self.config_issue_check_dict = {}
        self.fabric_node_ip_dict = {}
        self.configuration_issues = {}

        vrf_internal_subnet_dict = VrfInternalSubnet(self)
        vrf_internal_subnet_dict.build_vrf_internal_subnet_dict()
        endpoint_dict = EndpointDict(self)
        endpoint_dict.build_endpoint_dict()
        subject_filter_entry = SubjectFilterEntry(self)
        subject_filter_entry.build_subject_filter_entry_dict()
        l3out_dict = L3outDict(self)
        l3out_dict.build_l3out_dict()
        application_epg = ApplicationEpg(self)
        application_epg.build_application_epg_dict()
        contract_epg = ContractEpg(self)
        contract_epg.build_contract_epg_dict()
        external_epg = ExternalEpg(self)
        external_epg.build_external_epg_dict()
        l3out_vrf = L3outVrf(self)
        l3out_vrf.build_l3out_vrf_dict()
        bridge_domain = BridgeDomain(self)
        bridge_domain.build_bd_dict()
        config_snapshot = CheckConfigSnapshot(self)
        config_snapshot.build_config_snapshot_dict()
        top_system = TopSystem(self)
        top_system.build_top_system_dict(self)
        self.epg = EpgBd(self)
        self.epg.build_tenant_networking_epg_dict_table(self)
        static_routes = StaticRoutes(self)
        static_routes.build_static_routes_dict(self)
        self.contract_filter = ContractFilter(self)
        self.contract_filter.build_contract_filter_dict(self)
        epg_contract = EpgContract(self)
        epg_contract.build_epg_contract_consumer_provider_mapping_dict()
        # self.epg_bd_subnet_with_endpoints_dict = deepcopy(self.epg_bd_subnet_dict)
        self.contract_filter_no_endpoints_dict = deepcopy(self.contract_filter_dict)
        # self.epg_endpoint = AddEndpoint(self)
        # self.epg_endpoint.build_add_endpoint_dict(self)
        self.vzany_info = VzAny(self)
        self.vzany_info.build_vzany_dict(self)
        self.fabric_interface = FabricInterface(self)
        self.fabric_interface.build_fabric_interface_dict(self)
        self.fabric_node = FabricNode(self)
        self.fabric_node.build_fabric_node_ip_dict(self)
        self.lldp_neighbor = LldpNeighbor(self)
        self.lldp_neighbor.build_lldp_neighbor_dict(self)
        self.vpc_interface = VpcInterface(self)
        self.vpc_interface.build_vpc_interface_dict(self)
        self.vlan_pool = VlanPool(self)
        self.vlan_pool.build_vlan_pool_dict(self)
        self.epg_vpc = EpgVpc(self)
        self.epg_vpc.build_epg_vpc_dict(self)
        self.bgp_peer = BgpPeer(self)
        self.bgp_peer.build_bgp_peer_dict(self)
        self.ospf_neighbor = OspfNeighbor(self)
        self.ospf_neighbor.build_ospf_neighbor_dict(self)

        if self.appcentric_vrf_validation and config.env in config.cfg.get('appcentric_vrf_validation_env_list').split():
            for self.vrf in self.appcentric_vrf_list:
                self.vrf_name = self.vrf.split('/ctx-')[-1]
                self.vrf_external_epg_base_dict = defaultdict(dict)
                self.vrf_internal_epg_base_dict = defaultdict(dict)
                self.epg_base = EpgBase(self)
                self.epg_base.build_epg_base_dict(self)

                self.internal_or_external = 'external'
                self.vrf_epg_dict = deepcopy(self.vrf_external_epg_base_dict)
                self.external_epg_consumer = ConsumerContract(self)
                # self.external_epg_consumer_contract_dict = self.external_epg_consumer.build_consumer_epg_contract_dict(self)
                self.external_epg_consumer_contract_dict = self.external_epg_consumer.build_consumer_epg_contract_dict(self)
                write_file(f'{self.output_directory}/{self.vrf_name}_External_EPG_consumer_contract_no_endpoints_parsed.txt', self.external_epg_consumer_contract_dict)
                # write_file(f'{self.output_directory}/{self.vrf_name}_External_EPG_consumer_contract_with_endpoints_parsed.txt', self.external_epg_consumer_contract_with_endpoints_dict)
                self.external_epg_provider = ProviderContract(self)
                self.external_epg_provider_contract_dict = self.external_epg_provider.build_provider_epg_contract_dict(self)
                write_file(f'{self.output_directory}/{self.vrf_name}_External_EPG_provider_contract_parsed.txt', self.external_epg_provider_contract_dict)

                self.external_subnet_epg_source_no_endpoints_dict = deepcopy(self.external_epg_consumer_contract_dict)
                # self.external_subnet_epg_source_with_endpoints_dict = deepcopy(self.external_epg_consumer_contract_with_endpoints_dict)
                self.external_subnet_epg_import_security_no_endpoints_dict = defaultdict(dict)
                # self.external_subnet_epg_import_security_with_endpoints_dict = defaultdict(dict)
                self.external_subnet_epg_import_rtctrl_dict = defaultdict(dict)
                self.external_subnet_epg_export_rtctrl_dict = defaultdict(dict)
                self.external_subnet_epg_shared_security_dict = defaultdict(dict)
                self.external_subnet_epg_shared_rtctrl_dict = defaultdict(dict)
                self.external_subnet_to_epg_consumer = ExternalSubnet(self)
                self.external_subnet_to_epg_consumer.build_external_subnet_epg_dict(self)
                write_file(f'{self.output_directory}/{self.vrf_name}_External_Subnets_to_EPG_as_consumer_import_security_no_endpoints_parsed.txt', self.external_subnet_epg_import_security_no_endpoints_dict)
                # write_file(f'{self.output_directory}/{self.vrf_name}_External_Subnets_to_EPG_as_consumer_import_security_with_endpoints_parsed.txt', self.external_subnet_epg_import_security_with_endpoints_dict)
                write_file(f'{self.output_directory}/{self.vrf_name}_External_Subnets_to_EPG_import_rtctrl_parsed.txt', self.external_subnet_epg_import_rtctrl_dict)
                write_file(f'{self.output_directory}/{self.vrf_name}_External_Subnets_to_EPG_export_rtctrl_parsed.txt', self.external_subnet_epg_export_rtctrl_dict)
                write_file(f'{self.output_directory}/{self.vrf_name}_External_Subnets_to_EPG_shared_security_parsed.txt', self.external_subnet_epg_shared_security_dict)
                write_file(f'{self.output_directory}/{self.vrf_name}_External_Subnets_to_EPG_shared_rtctrl_parsed.txt', self.external_subnet_epg_shared_rtctrl_dict)

                self.internal_or_external = 'internal'
                self.vrf_epg_dict = deepcopy(self.vrf_internal_epg_base_dict)
                self.internal_epg_consumer = ConsumerContract(self)
                self.internal_epg_consumer_contract_dict = self.internal_epg_consumer.build_consumer_epg_contract_dict(self)
                write_file(f'{self.output_directory}/{self.vrf_name}_Internal_EPG_consumer_contract_no_endpoints_parsed.txt', self.internal_epg_consumer_contract_dict)
                # write_file(f'{self.output_directory}/{self.vrf_name}_Internal_EPG_consumer_contract_with_endpoints_parsed.txt', self.internal_epg_consumer_contract_with_endpoints_dict)
                self.internal_epg_provider = ProviderContract(self)
                self.internal_epg_provider_contract_dict = self.internal_epg_provider.build_provider_epg_contract_dict(self)
                write_file(f'{self.output_directory}/{self.vrf_name}_Internal_EPG_provider_contract_parsed.txt', self.internal_epg_provider_contract_dict)

        self.vrf_route = VrfRoute(self)
        self.vrf_route.build_vrf_route_dict(self)

        # self.rule = ConcreteRule(self)
        # self.rule.build_node_access_rule_dict(self)

        write_file(f'{self.output_directory}/Configuration_issues_to_check_parsed.txt', self.config_issue_check_dict)


