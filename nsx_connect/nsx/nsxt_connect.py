#!/usr/bin/python3
import sys

print(sys.path)

sys.path.append('/Users/jsmith/Documents/GitHub/Maestro2_0/nsx_connect')

# print(sys.path[-1])

import os
import inspect
print("this file: ",os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
print("this file: ",os.path.abspath(inspect.getfile(inspect.currentframe())))
print("this file: ",os.path.dirname(inspect.getfile(inspect.currentframe())))

from urllib3.exceptions import InsecureRequestWarning
import urllib3
import json
import requests.packages
import time

from Includes.MyParser import myJSONParser as mp
import Includes.db as db


################################################################################
##   API controller for NSX-T
##   Issues:
##      1.  No connectivity to external networks (internet sites) - Done
##      2.  Add DHCP configurations - Done
##      3.  Add DNS Configurations - Done
##      4.  Add Firewall Configurations - 
##      5.  Add DNAT configurations - Done
################################################################################


def getLS(man,auth=None,objectId=None,fileName=None):
    '''
    Description:
        This Function returns the configuration for all logical switches (not segments)
    Required arguments:
        man => string; NSX-T manager IP (Cluster IP preferred)

    Future improvements:
        provide the ability to grab a specific switch configuration
    '''

    url = "https://"+man+"/api/v1/logical-switches"

    payload = {}
    headers = {
      'Authorization': auth
    }

    response = requests.request("GET", url, headers=headers, data = payload, verify = False).json()

    mp(response)
    return(response)

def getLR(man,auth=None,objectId=None,fileName=None):
    '''
    Description:
        This Function returns the configuration for all logical routers
    Required arguments:
        man => string; NSX-T manager IP (Cluster IP preferred)

    Future improvements:
        provide the ability to grab a specific switch configuration
    '''
    url = "https://"+man+"/api/v1/logical-routers"

    payload = {}
    headers = {
      'Authorization': auth
    }

    response = requests.request("GET", url, headers=headers, data = payload, verify = False).json()

    mp(response)
    return(response)

def getSegments(man,auth=None,objectId=None,fileName=None):
    '''
    Description:
        This Function returns the configuration for all logical segments (not switches)
    Required arguments:
        man => string; NSX-T manager IP (Cluster IP preferred)

    Future improvements:
        provide the ability to grab a specific switch configuration
    '''
    if objectId==None:
        url = "https://"+man+"/policy/api/v1/infra/segments/"
    else:
        url = "https://"+man+"/policy/api/v1/infra/segments/" + objectId
    print(url)
    payload = {}
    headers = {
        'Authorization': auth
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def getTier0(man,auth=None,objectId=None,fileName=None):
    '''
    Description:
        This Function returns the configuration for all Tier-0 (T0) Logical Routers.  Provide an objectId for specific T0
        configuration
    Required arguments:
        man => string; NSX-T manager IP (Cluster IP preferred)
    Optional argumnets:
        objectId => string; T0 Logical Router ID for
    Future improvements:
        TBD
    '''
    if objectId==None:
        url = "https://"+man+"/policy/api/v1/infra/tier-0s/"
    else:
        url = "https://"+man+"/policy/api/v1/infra/tier-0s/" + objectId
    print(url)
    payload = {}
    headers = {
        'Authorization': auth
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def getTier1(man,auth=None,objectId=None,fileName=None):
    '''
        Description:
            This Function returns the configuration for all Tier-1 (T1) Logical Routers.  Provide an objectId for
            specific T1 configuration
        Required arguments:
            man => string; NSX-T manager IP (Cluster IP preferred)
        Optional argumnets:
            objectId => string; T0 Logical Router ID for
        Future improvements:
            TBD
        '''
    if objectId==None:
        url = "https://"+man+"/policy/api/v1/infra/tier-1s/"
    else:
        url = "https://"+man+"/policy/api/v1/infra/tier-1s/" + objectId
    print(url)
    payload = {}
    headers = {
        'Authorization': auth
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def getTransportNode(man,auth=None,objectId=None,fileName=None):
    '''
        Description:
            This Function returns the configuration for all Transport Nodes (host and edge) Logical Routers.
            Provide an objectId for specific Transport Node configuration
        Required arguments:
            man => string; NSX-T manager IP (Cluster IP preferred)
        Optional argumnets:
            objectId => string; T0 Logical Router ID for
        Future improvements:
            TBD
        '''
    if objectId==None:
        url = "https://"+man+"/api/v1/transport-nodes/"
    else:
        url = "https://"+man+"/api/v1/transport-nodes/" + objectId
    print(url)
    payload = {}
    headers = {
        'Authorization': auth
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def getEdgeCluster(man,auth=None,objectId=None,fileName=None):
    '''
        Description:
            This Function returns the configuration for all Edge Clusters.  Provide an objectId for
            specific Edge Cluster configuration
        Required arguments:
            man => string; NSX-T manager IP (Cluster IP preferred)
        Optional argumnets:
            objectId => string; T0 Logical Router ID for
        Future improvements:
            TBD
        '''
    if objectId==None:
        url = "https://"+man+"/api/v1/edge-clusters/"
    else:
        url = "https://"+man+"/api/v1/edge-clusters/" + objectId
    print(url)
    payload = {}
    headers = {
        'Authorization': auth
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def getT0NATRules(man,auth=None,objectId='',natRuleId=None,fileName=None):
    '''
        Description:
            This Function returns the configuration for all Tier-0 NAT Rules.  Provide an objectId for specific T0
            NAT configuration.  Also include a natRuleId for specific NAT rule configuration of TO.
        Required arguments:
            man => string; NSX-T manager IP (Cluster IP preferred)
            objectId => string; T0 Logical Router ID
        Optional argumnets:
            natRuleId => string; T0 Logical Router NAT rule ID
        Future improvements:
            TBD
        '''
    if natRuleId==None:
        url = "https://"+man+"/policy/api/v1/infra/tier-0s/"+objectId+"/nat/USER/nat-rules"
    else:
        url = "https://"+man+"/policy/api/v1/infra/tier-0s/"+objectId+"/nat/USER/nat-rules"+natRuleId
    print(url)
    payload = {}
    headers = {
        'Authorization': auth
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def getBGP(man,auth=None,objectId="",fileName=None):
    '''
        Description:
            This Function returns the BGP configuration for a specific Tier-0 Logical Router.
            Provide an objectId for specific T0 configuration
        Required arguments:
            man => string; NSX-T manager IP (Cluster IP preferred)
        Optional argumnets:
            objectId => string; T0 Logical Router ID for
        Future improvements:
            TBD
        '''
    url = "https://"+man+"/policy/api/v1/infra/tier-0s/"+objectId+"/locale-services/xxx2-locale-services/bgp"
    print(url)
    payload = {}
    headers = {
        'Authorization': auth
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def getBGPNeighbors(man,auth=None,objectId="",fileName=None):
    '''
        Description:
            This Function returns the BGP Neighbor configuration for a specified Tier-0 Logical Routers.
            Provide an objectId for specific T0 configuration
        Required arguments:
            man => string; NSX-T manager IP (Cluster IP preferred)
        Optional argumnets:
            objectId => string; T0 Logical Router ID for
        Future improvements:
            TBD
        '''
    url = "https://"+man+"/policy/api/v1/infra/tier-0s/"+objectId+"/locale-services/xxx2-locale-services/bgp/neighbors"
    print(url)
    payload = {}
    headers = {
        'Authorization': auth
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def getEdgeStatus(edged_id,auth):
    '''
        Description:
            This Function returns the configuration for all Tier-0 Logical Routers.  Provide an objectId for specific T0
            configuration
        Required arguments:
            man => string; NSX-T manager IP (Cluster IP preferred)
        Optional argumnets:
            objectId => string; T0 Logical Router ID for
        Future improvements:
            TBD
            TBD
        '''
    url = "https://"+man+"/api/v1/transport-nodes/"+edged_id+"/state"
    # print(url)
    payload = {}
    headers = {
        'Authorization': auth
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def createLS(man, payload, auth=None, objectId=None):
    url = "https://" + man + "/api/v1/logical-switches"

    headers = {
        'Authorization': auth
    }

    response = requests.request("POST", url, headers = headers, data = payload, verify = False).json()

    mp(response)
    return (response)


def confSegment(man, payload, auth=None, objectId=None):
    url = "https://" + man + "/policy/api/v1/infra/segments/" + objectId
    print(url)

    headers = {
        'Authorization': auth,
        'Content-type' : 'application/json;charset=UTF-8'
    }

    response = requests.request("PUT", url, headers = headers, data = payload, verify = False).json()

    mp(response)
    return (response)


def confTier0(man, payload, auth=None, objectId=None):
    url = "https://" + man + "/policy/api/v1/infra/tier-0s/" + objectId
    print(url)

    headers = {
        'Authorization': auth,
        'Content-type' : 'application/json;charset=UTF-8'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def confTier1(man, payload, auth=None, objectId=None):
    if objectId == None:
        url = "https://" + man + "/policy/api/v1/infra/tier-1s/"
    else:
        url = "https://" + man + "/policy/api/v1/infra/tier-1s/" + objectId
    print(url)

    headers = {
        'Authorization': auth,
        'Content-type': 'application/json;charset=UTF-8'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def confLocServ(man, payload, lr_id, auth=None, objectId='default',mode=0):
    if mode == 0:
        url = "https://" + man + "/policy/api/v1/infra/tier-0s/"+lr_id+"/locale-services/"+ objectId
    elif mode == 1:
        url = "https://" + man + "/policy/api/v1/infra/tier-1s/"+lr_id+"/locale-services/"+ objectId
    print(url)
    cont=False

    headers = {
        'Authorization': auth,
        'Content-type': 'application/json;charset=UTF-8'
    }

    while cont == False:
        response = requests.request("PUT", url, headers=headers, data=payload, verify=False).json()
        if 'httpStatus' in response.keys():
            time.sleep(30)
        else:
            cont = True

    mp(response)
    return (response)

def confLRInts(man,payload,mode,lr_id,loc_srv='default',auth=None,objectId=''):
    url = "https://"+man+"/policy/api/v1/infra/"+mode+"/"+lr_id+"/locale-services/"+loc_srv+"/interfaces/"+objectId
    print(url)

    headers = {
        'Authorization': auth,
        'Content-type': 'application/json;charset=UTF-8'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def confTransportNode(man, payload, auth=None, objectId=None):
    url = "https://" + man + "/api/v1/transport-nodes/"
    print(url)

    headers = {
        'Authorization': auth,
        'Content-type': 'application/json;charset=UTF-8'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def confEdgeCluster(man, payload, auth=None, objectId=None):
    url = "https://" + man + "/api/v1/edge-clusters/"

    print(url)

    headers = {
        'Authorization': auth,
        'Content-type': 'application/json;charset=UTF-8'
    }
    cont = False
    while cont == False:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()
        if 'httpStatus' in response.keys():
            time.sleep(30)
        else:
            cont = True
    # response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def confNATRules(man, auth, payload, objectId,natRuleId):
    url = "https://" + man + "/policy/api/v1/infra/tier-0s/" + objectId + "/nat/USER/nat-rules/" + natRuleId
    print(url)

    headers = {
        'Authorization': auth,
        'Content-type': 'application/json;charset=UTF-8'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def confBGP(man, payload, mode, lr_id, auth=None, objectId=None):
    url = "https://" + man + "/policy/api/v1/infra/"+mode+"/" + lr_id + "/locale-services/default/bgp"

    print(url)

    headers = {
        'Authorization': auth,
        'Content-type': 'application/json;charset=UTF-8'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def confBGPNeigh(man,payload,mode,lr_id,loc_srv='default',auth=None,objectId=''):
    url = "https://" + man + "/policy/api/v1/infra/" + mode + "/" + lr_id + "/locale-services/" + loc_srv \
          + "/bgp/neighbors/" + objectId
    print(url)

    headers = {
        'Authorization': auth,
        'Content-type': 'application/json;charset=UTF-8'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def confDHCPPro(man,payload,auth):
    url = "https://" + man + "/api/v1/dhcp/server-profiles"
    print(url)

    headers = {
        'Authorization': auth,
        'Content-type': 'application/json;charset=UTF-8'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def confDHCPSvr(man,payload,auth,d_id):
    url = "https://" + man + "/policy/api/v1/infra/dhcp-server-configs/"+d_id
    print(url)

    headers = {
        'Authorization': auth,
        'Content-type': 'application/json;charset=UTF-8'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def confDNSServer(man,payload,lr_id,auth):
    url = "https://" + man + "/policy/api/v1/infra/tier-1s/"+lr_id+"/dns-forwarder"
    print(url)

    headers = {
        'Authorization': auth,
        'Content-type': 'application/json;charset=UTF-8'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, verify=False).json()

    mp(response)
    return (response)

def buildSegment(tc,mode='',type=None,i=None):
    '''
        Description:
            This Function builds the configuration for a new interface and returns the new
            configuration to the calling function.
        Required arguments:
            tc => string; tenant code
            mode => string; l3 for a linked segment and l2 for a non-linked segment
        Future improvements:
            TBD
    '''
    if mode == 'l2':
        data = {
              "type": "DISCONNECTED",
              "transport_zone_path": "/infra/sites/default/enforcement-points/default/transport-zones/e61b02d4-b31c-48f2-b5bb-3a56f2ac3c05",
              "advanced_config": {
                "address_pool_paths": [],
                "hybrid": False,
                "local_egress": False,
                "connectivity": "ON"
              },
              "resource_type": "Segment",
              "id": tc+"-seg-t0t0-gw0"+i,
              "display_name": tc+"-seg-t0t0-gw0"+i
            }
    elif mode == 'l3':
        if i=='prod':
            gw = '192.168.162.1/24'
            dhcp = '192.168.162.100-192.168.162.200'
            net = '192.168.162.0/24'
        elif i=='dev':
            gw = '192.168.163.1/24'
            dhcp = '192.168.163.64-192.168.163.200'
            net = '192.168.163.0/24'
        data = {
            "type": "ROUTED",
            "subnets": [
                {
                    "gateway_address": gw,
                    "dhcp_ranges": [
                        dhcp
                    ],
                    "network": net
                }
            ],
            "connectivity_path": "/infra/tier-1s/okr01-c01-"+tc+"-t1-"+i,
            "transport_zone_path": "/infra/sites/default/enforcement-points/default/transport-zones/e61b02d4-b31c-48f2-b5bb-3a56f2ac3c05",
            "advanced_config": {
                "address_pool_paths": [],
                "hybrid": False,
                "local_egress": False,
                "connectivity": "ON"
            },
            "resource_type": "Segment",
            "id": tc+"-seg-"+i,
            "display_name": tc+"-seg-"+i
            }
    return data

def buildLRInterface(tc: str, ip: str, inst: str, type: str = 'pro', edcl_id:str='', edge_id:str='') -> object:
    '''
    Description:
        This Function builds the configuration for a new interface and returns the new
        configuration to the calling function.
    Required arguments:
        tc => string; tenant code
        mode => t0 for Tier-0 interface and t1 for Tier-1 interface
        type => string; upl for uplink interface and dol for downlink (LAN/DMZ) interface
        lrid => string; Logical Router Id
        locserv => string; Locale-Service Id
    Future improvements:
        provide the ability to create a service interface
    '''
    if type == 'pro':
        data = {
          "mtu": 1500,
          "edge_path": "/infra/sites/default/enforcement-points/default/edge-clusters/75696caf-e26a-4785-920d-a38f0c9f0ef9/edge-nodes/"+edge_id,
          "segment_path": "/infra/segments/"+tc+"-seg-t0t0-gw0"+inst,
          "type": "EXTERNAL",
          "resource_type": "Tier0Interface",
          "id": "to-"+tc+"-0"+inst,
          "display_name": "to-"+tc+"-0"+inst,
          "subnets": [
            {
              "ip_addresses": [
                ip.split('/')[0]
              ],
              "prefix_len": ip.split('/')[1]
            }
          ]
        }
    elif type=='ten':
        segpath="/infra/segments/okr01-c01-tenant-uplinks"

        if int(inst)>1:
            segpath = "/infra/segments/okr01-c01-tenant-uplink0"+inst

        data = {
          "mtu": 1500,
          "edge_path": "/infra/sites/default/enforcement-points/default/edge-clusters/"+edcl_id+"/edge-nodes/"+edge_id,
          "segment_path": segpath,
          "type": "EXTERNAL",
          "resource_type": "Tier0Interface",
          "id": "to-provider-0"+inst,
          "display_name": "to-provider-0"+inst,
          "subnets": [
            {
              "ip_addresses": [
                ip.split('/')[0]
              ],
              "prefix_len": ip.split('/')[1]
            }
          ]
        }
    return(data)

def buildBGP(tc,mode='',s_ip='',n_ip='',n_as='',inst='',type=None):
    '''
    Description:
        This Function builds the configuration for a BGP global configuration or
        neighbor configuration and returns the new configuration to the calling function.
    Required arguments:
        tc => string; tenant code
        mode => string; conf for bgp general configuration and neigh for bgp neigh configuration
        lrid => string; Logical Router Id
        locserv => string; Locale-Service Id
    Future improvements:
        TBD
    '''
    if mode == "neigh":
        if type=='ten':
            data = {
              "source_addresses": [
                s_ip
              ],
              "neighbor_address": n_ip,
              "remote_as_num": n_as,
              "route_filtering": [
                {
                  "enabled": True,
                  "address_family": "IPV4"
                }
              ],
              "keep_alive_time": 10,
              "hold_down_time": 30,
              "bfd": {
                "enabled": False,
                "interval": 1000,
                "multiple": 3
              },
              "allow_as_in": False,
              "maximum_hop_limit": 1,
              "resource_type": "BgpNeighborConfig",
              "id": "to-provider-0"+inst,
              "display_name": "to-provider-0"+inst
              }
        else:
            data = {
                "source_addresses": [
                    s_ip
                ],
                "neighbor_address": n_ip,
                "remote_as_num": n_as,
                "in_route_filters": [
                    "/infra/tier-0s/okr01-c01-prov01/prefix-lists/no-privates"
                ],
                "out_route_filters": [
                    "/infra/tier-0s/okr01-c01-prov01/prefix-lists/no-privates"
                ],
                "route_filtering": [
                    {
                        "enabled": True,
                        "address_family": "IPV4"
                    }
                ],
                "keep_alive_time": 10,
                "hold_down_time": 30,
                "bfd": {
                    "enabled": False,
                    "interval": 1000,
                    "multiple": 3
                },
                "allow_as_in": False,
                "maximum_hop_limit": 1,
                "resource_type": "BgpNeighborConfig",
                "id": "to-" + tc + "-0" + inst,
                "display_name": "to-" + tc + "-0" + inst
            }

    else:
        ecmp=True
        if type=='ten':
            ecmp=False
        data = {
            "local_as_num": n_as,
            "enabled": True,
            "ecmp": ecmp,
            "multipath_relax": True,
            "graceful_restart_config": {
                "mode": "DISABLE",
                "timer": {
                    "restart_timer": 180,
                    "stale_route_timer": 600
                }
            },
            "resource_type": "BgpRoutingConfig",
            "id": "bgp",
            "display_name": "bgp"
            }
    return(data)

def buildEdge(tc,mode='', ip_addr='', gw='', inst='' ):
    '''
    Description:
        This Function builds the configuration for a new interface and returns the new
        configuration to the calling function.
    Required arguments:
        tc => string; tenant code
        type => string; vm for Edge VM configuration and bg for bare-metal edge configurations
        mode => string; new to for new edge deployment and upd to update existing edge configurations
    Future improvements:
        support bare-metal edge configurations
    '''
    data = {
        "host_switch_spec": {
            "host_switches": [
                {
                        "host_switch_name": "okr01-c01-nvds01",
                        "host_switch_id": "efd83a3b-e6b3-4754-a311-665253074961",
                        "host_switch_type": "NVDS",
                        "host_switch_mode": "STANDARD",
                        "host_switch_profile_ids": [
                            {
                                "key": "UplinkHostSwitchProfile",
                                "value": "df11a585-f9a2-4d59-ad38-737e2b45bc88"
                            },
                            {
                                "key": "LldpHostSwitchProfile",
                                "value": "9e0b4d2d-d155-4b4b-8947-fbfe5b79f7cb"
                            }
                        ],
                        "pnics": [
                            {
                                "device_name": "fp-eth0",
                                "uplink_name": "uplink-1"
                            },
                            {
                                "device_name": "fp-eth1",
                                "uplink_name": "uplink-2"
                            }
                        ],
                        "is_migrate_pnics": False,
                        "ip_assignment_spec": {
                            "ip_pool_id": "3f4c31b6-0554-44b9-9aec-0ea9b3d5673f",
                            "resource_type": "StaticIpPoolSpec"
                        },
                        "cpu_config": [],
                        "transport_zone_endpoints": [
                            {
                                "transport_zone_id": "e61b02d4-b31c-48f2-b5bb-3a56f2ac3c05",
                                "transport_zone_profile_ids": [
                                    {
                                        "resource_type": "BfdHealthMonitoringProfile",
                                        "profile_id": "52035bb3-ab02-4a08-9884-18631312e50a"
                                    }
                                ]
                            },
                            {
                                "transport_zone_id": "fe6e11a9-d41c-4fef-a9b7-f150e7609792",
                                "transport_zone_profile_ids": [
                                    {
                                        "resource_type": "BfdHealthMonitoringProfile",
                                        "profile_id": "52035bb3-ab02-4a08-9884-18631312e50a"
                                    }
                                ]
                            }
                        ],
                        "vmk_install_migration": [],
                        "pnics_uninstall_migration": [],
                        "vmk_uninstall_migration": [],
                        "not_ready": False
                    }
                ],
                "resource_type": "StandardHostSwitchSpec"
            },

            "maintenance_mode": "DISABLED",
            "node_deployment_info": {
                "deployment_type": "VIRTUAL_MACHINE",
                "deployment_config": {
                    "vm_deployment_config": {
                        "vc_id": "2224fbd4-831e-445b-b457-0f873a47e617",
                        "compute_id": "domain-c26",
                        "storage_id": "datastore-40",
                        "management_network_id": "42a3d6e0-5bf1-4b9f-bf09-18512f540c4b",
                        "management_port_subnets": [
                            {
                                "ip_addresses": [
                                    ip_addr
                                ],
                                "prefix_length": 24
                            }
                        ],
                        "default_gateway_addresses": [
                            gw
                        ],
                        "data_network_ids": [
                            "3197f5ad-2d38-4c8b-b2a9-a22efa961e6a",
                            "c62bc94e-ede7-41cf-be01-6bc4286513d7"
                        ],
                        "enable_ssh": True,
                        "allow_ssh_root_login": False,
                        "placement_type": "VsphereDeploymentConfig"
                    },
                    "form_factor": "SMALL",
                    "node_user_settings": {
                        "cli_username": "admin",
                        "cli_password": "ITaaSwins!!SAIC1811",
                        "audit_username": "audit",
                        "audit_password": "ITaaSwins!!SAIC1811",
                        "root_password": "ITaaSwins!!SAIC1811"
                    }
                },
                "node_settings": {
                    "hostname": tc+"-sdn-edge0"+inst,
                    "enable_ssh": True,
                    "allow_ssh_root_login": False
                },
                "resource_type": "EdgeNode",
                "display_name": tc+"-sdn-edge0"+inst,
                "description": "",
                "ip_addresses": [
                    ip_addr
                ]
            },
            "resource_type": "TransportNode",
            "display_name": tc+"-sdn-edge0"+inst
        }
    return(data)

def buildEdgeCluster(tc: str,edge_id1: str,edge_id2: str,inst: str):
    '''
    Description:
        This Function builds the configuration for an edge cluster and returns the new
        configuration to the calling function.
    Required arguments:
        tc => string; tenant code
        mode => string; new to create a new edge cluster and upd to update an existing edge cluster
    Future improvements:
        Need to grab edge id based on tc
        Provide a method to update existing edge clusters
    '''
    data = {
          "deployment_type": "VIRTUAL_MACHINE",
          "members": [
            {
              "transport_node_id": edge_id1
            },
            {
              "transport_node_id": edge_id2
            }
          ],
          "cluster_profile_bindings": [
            {
              "resource_type": "EdgeHighAvailabilityProfile",
              "profile_id": "91bcaa06-47a1-11e4-8316-17ffc770799b"
            }
          ],
          "member_node_type": "EDGE_NODE",
          "resource_type": "EdgeCluster",
          "display_name": tc+"-tenant-edcl0"+inst,
          "description": tc+" Edge Cluster"
        }
    return(data)

def buildLR(tc,mode,enc=None,d_id=None):
    '''
    Description:
        This Function builds the configuration for a logical router and returns the new
        configuration to the calling function.
    Required arguments:
        tc => string; tenant code
        mode => string; t0 for Tier-0 Logical Router configuration and t1 for Tier-1 Logical Router configurations
        lrid => string; Logical Router Id
    Future improvements:
        Provide a method to update existing logical routers
    '''
    if mode=='t0':
        data = {
              "transit_subnets": [
                "100.64.0.0/16"
              ],
              "internal_transit_subnets": [
                "169.254.0.0/28"
              ],
              "ha_mode": "ACTIVE_STANDBY",
              "failover_mode": "NON_PREEMPTIVE",
              "ipv6_profile_paths": [
                "/infra/ipv6-ndra-profiles/default",
                "/infra/ipv6-dad-profiles/default"
              ],
              "resource_type": "Tier0",
              "id": "okr01-c01-"+tc+"-t0",
              "display_name": "okr01-c01-"+tc+"-t0",
            }
    elif mode=='t1':
        data = {
              "tier0_path": "/infra/tier-0s/okr01-c01-"+tc+"-t0",
              "failover_mode": "NON_PREEMPTIVE",
              "enable_standby_relocation": False,
              "dhcp_config_paths": [
                "/infra/dhcp-server-configs/"+d_id
              ],
              "route_advertisement_types": [
                    "TIER1_NAT",
                    "TIER1_CONNECTED",
                    "TIER1_DNS_FORWARDER_IP"
              ],
              "force_whitelisting": False,
              "default_rule_logging": False,
              "disable_firewall": False,
              "ipv6_profile_paths": [
                "/infra/ipv6-ndra-profiles/default",
                "/infra/ipv6-dad-profiles/default"
              ],
              "resource_type": "Tier1",
              "id": "okr01-c01-"+tc+"-t1-"+enc,
              "display_name": "okr01-c01-"+tc+"-t1-"+enc
           }
    return(data)

def buildLocServ(tc,edcl,mode):
    '''
        Description:
            This Function builds the configuration for a logical routers locale services and returns the new
            configuration to the calling function.
        Required arguments:
            tc => string; tenant code
        Future improvements:
            Need to add a method to pull the specific edge cluster for the Logical Router (based on tc)
            Provide a method to update existing locale service
        '''
    data={}
    if mode == 't0':
        data = {
                  "edge_cluster_path": "/infra/sites/default/enforcement-points/default/edge-clusters/"+edcl,
                  "resource_type": "LocaleServices",
                  "id": "default",
                  "display_name": "default",
                  "description": tc+" Tenant Local-Services",
                  "route_redistribution_types": [
                    "TIER0_NAT",
                    "TIER0_CONNECTED",
                    "TIER0_STATIC",
                    "TIER1_NAT"
                  ]
            }
    elif mode == 't1':
        data = {
            "edge_cluster_path": "/infra/sites/default/enforcement-points/default/edge-clusters/" + edcl,
            "resource_type": "LocaleServices",
            "id": "default",
            "display_name": "default",
            "description": tc + " Tenant Locale-Services",
            "route_redistribution_types": [
                "TIER1_NAT",
                "TIER1_CONNECTED",
                "TIER1_STATIC",
                "TIER1_DNS_FORWARDER_IP"
            ]
        }
    return (data)

def buildNAT(tc, mode,t_net,s_net,inst,lr_id):
    '''
            Description:
                This Function builds the configuration for a logical routers NAT services and returns the new
                configuration to the calling function.
            Required arguments:
                tc => string; tenant code
                mode => string; t0 for Tier-0 Logical Router configuration and t1 for Tier-1 Logical Router configurations
                lrid => string; Logical Router Id
                locserv => string; Locale-Service Id of the Logical router
            Future improvements:
                Provide a method to update existing locale service
    '''
    data = {
          "sequence_number": 100,
          "action": "SNAT",
          "source_network": s_net,
          "service": "",
          "translated_network": t_net,
          "scope": [
            "/infra/tier-0s/"+lr_id+"/locale-services/default/interfaces/to-provider-01",
            "/infra/tier-0s/"+lr_id+"/locale-services/default/interfaces/to-provider-02"
          ],
          "enabled": True,
          "logging": True,
          "resource_type": "PolicyNatRule",
          "id": tc+"_nat_"+inst,
          "display_name": tc+"_nat_"+inst,
          "description": "Outbound NAT",
        }
    return (data)

def buildDHCPProfile(tc,edcl,enc,mode='t1'):
    data ={
      "edge_cluster_id": edcl,
      "enable_standby_relocation": False,
      "resource_type": "DhcpProfile",
      "id": tc+"-"+enc+"-dhcp-profile",
      "display_name": mode+"-"+enc+"-dhcp-profile",
      "description": "Common DHCP server profile for Policy Manager"
      }
    return(data)

def buildDHCPServer(tc,enc,edcl):
    if enc == 'prod':
        svr_add='10.1.1.2/24'
    elif enc == 'dev':
        svr_add='10.1.2.2/24'
    data = {
        "server_address": svr_add,
        "lease_time": 86400,
        "edge_cluster_path": "/infra/sites/default/enforcement-points/default/edge-clusters/"+edcl,
        "id": tc+"-"+enc+"-dhcp-01",
        "display_name": tc+"-"+enc+"-dhcp-01"
    }
    return(data)

def buildDNSServer(tc,enc):
    if enc == 'prod':
        svr_add = '10.1.3.2'
    elif enc == 'dev':
        svr_add = '10.1.4.2'
    data = {
        "listener_ip": svr_add,
        "default_forwarder_zone_path": "/infra/dns-forwarder-zones/default",
        "log_level": "INFO",
        "enabled": True,
        "resource_type": "PolicyDnsForwarder",
        "id": "dns-forwarder",
        "display_name": tc + "-"+enc+"-dns-01",
        "description": "DNS for " + tc +" "+enc+" Tenant",
        "marked_for_delete": False
    }
    return(data)

if __name__ == "__main__":
    to_t = time.time()
    st_t = time.time()
    urllib3.disable_warnings(InsecureRequestWarning)
    #uname = input('Username:  ')
    #passw = input('Password:  ')
    #auth_nsx = nsx('admin', 'ITaaSwins!!SAIC1811')
    auth_nsx = 'Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ=='
    auth_vc = 'Basic YWRtaW5pc3RyYXRvckB2c3BoZXJlLmxvY2FsOlZNd2FyZTEh'
  
    man = '172.16.11.30'
    vman = '172.16.11.64'

    animation = [".","..","...","....",".....","....","...","..","."]
    idx = 0
    # vcookie = vapi.getAuth(vman, auth_vc)
 
    #man = input("NSX-T Manager IP:  ")
    #uname = ("Username:  ")
    #passw = ("Password:  ")
    native = ""
    native_mode = False
    tc = ""

    if "=" not in "!":
        print("test passed")
    
    if len(sys.argv) == 1:
        print("Argument passed")
        print("Before we begin, lets collect some information on your environment...")
        tc = input("Tenant Code (2 to 4 character tenant ID):  ")

        check = ['Y','Yes',"YES","yes","y","n",'N',"no","No","NO","Q","q","quit","Quit","QUIT","quit"]
        while native not in check:
            print("My Choice:  " + native)
            print("My Check:  " + str(check))
            native = input("Are you going Native today (yes or no)?:  ")
            if native in ['Y','y','Yes',"YES","yes"]:
                native_mode = True
                print("Run in Native mode (Deploy from this script) :" +native_mode)
            elif native in ['N','n','No',"NO","no"]:
                native_mode = False
                print(native_mode)
            elif native in ['Q','q','Quit',"QUIT","quit"]:
                print(native)
                quit()
    elif("=" not in str(sys.argv) or "nm=" not in str(sys.argv) or "tc=" not in str(sys.argv)):
        print("error with inputs, arguments must be nm=[true|false] and tc=[tenant code]...all or nothing")
    else:
        print(sys.argv)
        for arg in sys.argv:
            print(arg.split('=')[0])
            if arg.split('=')[0] == "nm":
                nm = arg.split('=')[1]
            elif arg.split('=')[0] == "tc":
                tc = arg.split('=')[1]

        if nm == "true":
            native_mode = True
        elif nm == "false":
            native_mode = False
        else:
            print("Error:  nm should be set to 'true' or 'false'")
            quit()
        print("nm => " + nm)
        print("tc => " + tc)

        run = False
 #       native_mode = True if native in ['Y','Yes',"YES","yes"]
 #       native_mode = False if native in ['N', 'No', "NO", "no"]
 #       return if native in ['Q','QUIT','Quit','quit']

    '''
    Get IP addresses for Tenant Deployment
    '''
    ## Previously created two additional Logical Segments, but due to the limit of 16 interfaces, this became a less
    ## a less than scalable approach.  The new approach is to create/utilize a /24 network for tenant peering.  This
    ## will allow for up to 253 peers (tenants) per interface x15 available interfaces to downstream peers
    # pri_net1 = db.getSubnets(None,None,'pr')
    # print("Tenant T0 Transit Network #1:  "+pri_net1)
    # db.updSubnets(tc,pri_net1.split("/")[0])
    # pri_ips1 = db.getHostIP(pri_net1)
    # print("Host IPs:  "+str(pri_ips1))
    # db.inAddresses(pri_ips1,pri_net1.split('/')[1],pri_net1.split('/')[0],tc)
    #
    # pri_net2 = db.getSubnets(None, None, 'pr')
    # print("Tenant T0 Transit Network #2:  "+pri_net2)
    # db.updSubnets(tc, pri_net2.split("/")[0])
    # pri_ips2 = db.getHostIP(pri_net2)
    # db.inAddresses(pri_ips2, pri_net2.split('/')[1], pri_net2.split('/')[0], tc)

    pri_ips1 = db.getAddresses('','192.168.164.0')
    print(pri_ips1)
    db.updAddresses(tc, pri_ips1[0][0])
    print("Tenant T0 Transit IP 1:  "+pri_ips1[0][0])

    pri_ips2 = db.getAddresses('','192.168.165.0')
    db.updAddresses(tc, pri_ips2[0][0])
    print("Tenant T0 Transit IP 1:  "+pri_ips2[0][0])

    pub_net1 = db.getSubnets(None, None, 'pu')
    print("Tenant T0 Public Network #1:  "+pub_net1)
    db.updSubnets(tc, pub_net1.split("/")[0])
    pub_ips = db.getHostIP(pub_net1)
    db.inAddresses(pub_ips, pub_net1.split('/')[1], pub_net1.split('/')[0], tc)
    nat_ip = db.getAddresses(tc,pub_net1.split('/')[0])
    db.updAddresses(tc,nat_ip[0][0],'nat')
    print(nat_ip)

    proBGPAS = 65000
    tenBGPAS = db.getBGPAS()
    db.updBGPAS(tc,tenBGPAS)

    edge1_ip = db.getAddresses('sddc','172.16.31.0')
    db.updAddresses(tc, edge1_ip[0][0])
    print("Edge 1 MGMT IP:  "+edge1_ip[0][0])

    edge2_ip = db.getAddresses('sddc','172.16.31.0')
    db.updAddresses(tc, edge2_ip[0][0])
    print("Edge 2 MGMT IP:  "+edge2_ip[0][0])

    print(db.getSubnets(tc))

    if(native_mode):
        print('**********************************************************')
        print("Provider T0 - BGP Neighbor Configuration 1")
        print('**********************************************************')
        pro_neigh1 = buildBGP(tc, 'neigh', pri_ips1[0][3],pri_ips1[0][0].split('/')[0],tenBGPAS,'1','pro')
        mp(pro_neigh1)
        print("----------------------")
        print(json.dumps(pro_neigh1))
        pro_neigh1 = confBGPNeigh(man, json.dumps(pro_neigh1), 'tier-0s', 'okr01-c01-prov01',
                                'default',auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==', objectId=pro_neigh1['id'])

        print('**********************************************************')
        print("Provider T0 - BGP Neighbor Configuration 2")
        print('**********************************************************')
        pro_neigh2 = buildBGP(tc, 'neigh', pri_ips2[0][3],pri_ips2[0][0].split('/')[0],tenBGPAS,'2','pro')
        mp(pro_neigh2)
        print("----------------------")
        print(json.dumps(pro_neigh2))
        pro_neigh2 = confBGPNeigh(man, json.dumps(pro_neigh2), 'tier-0s', 'okr01-c01-prov01',
                                'default',auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==', objectId=pro_neigh2['id'])

    
    print('**********************************************************')
    print("Tenant -  Edge 1 Configuration")
    print('**********************************************************')
    t_edge1 = buildEdge(tc, '', edge1_ip[0][0].split('/')[0], edge1_ip[0][3], '1')
    mp(t_edge1)
    print("----------------------")
    print(json.dumps(t_edge1))
    
    if run:
        t_edge1 = confTransportNode(man, json.dumps(t_edge1), auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==', objectId=None)

    print('**********************************************************')
    print("Tenant -  Edge 2 Configuration")
    print('**********************************************************')
    t_edge2 = buildEdge(tc, '', edge2_ip[0][0].split('/')[0], edge2_ip[0][3], '2')
    mp(t_edge2)
    print("----------------------")
    print(json.dumps(t_edge2))
    if run:
        t_edge2 = confTransportNode(man, json.dumps(t_edge2), auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==', objectId=None)

    if run:
        print('**********************************************************')
        print("Tenant - Edge State")
        print('**********************************************************')
        t_edge1_state = getEdgeStatus(t_edge1['id'],auth_nsx)
        t_edge2_state = getEdgeStatus(t_edge2['id'],auth_nsx)

        while (t_edge1_state['state'] != 'success' or t_edge1_state['state'] == 'pending' or t_edge1_state['state'] == 'failed') \
                or (t_edge2_state['state'] != 'success' or t_edge2_state['state'] == 'pending' or t_edge2_state['state'] == 'failed'):
            t_edge1_state = getEdgeStatus(t_edge1['id'],auth_nsx)
            t_edge2_state = getEdgeStatus(t_edge2['id'],auth_nsx)

            print(animation[idx % len(animation)], end='\n\r')
            time.sleep(30)
            idx+=1

        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1!')
        print(t_edge1_state['state'])
        print(t_edge2_state['state'])
        print('**********************************************************')
        print("Tenant - Edge Cluster Configuration")
        print('**********************************************************')
        t_edcl = buildEdgeCluster(tc, t_edge1['id'], t_edge2['id'],'1')
        mp(t_edcl)
        print("----------------------")
        print(json.dumps(t_edcl))
        t_edcl = confEdgeCluster(man, json.dumps(t_edcl), auth=auth_nsx, objectId=None)

    if (native_mode):
        print('**********************************************************')
        print("Tenant T0 - LR Configuration")
        print('**********************************************************')
        t_t0_1 = buildLR(tc,'t0')
        mp(t_t0_1)
        print("----------------------")
        print(json.dumps(t_t0_1))
        t_t0_1 = confTier0(man, json.dumps(t_t0_1), auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==', objectId=t_t0_1['id'])

        print('**********************************************************')
        print("Tenant T0 - LR Locale Services Global  Configuration")
        print('**********************************************************')
        print("Building Local-Service...")
        t_locsrv_1 = buildLocServ(tc,t_edcl['id'],'t0')
        mp(t_locsrv_1)
        print("----------------------")
        print(json.dumps(t_locsrv_1))
        t_locsrv_1 = confLocServ(man, json.dumps(t_locsrv_1), t_t0_1['id'], auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==', objectId='default',mode=0)

        print('**********************************************************')
        print("Tenant T0 - LR Interface 1 Configuration")
        print('**********************************************************')
        ten_int1 = buildLRInterface(tc,pri_ips1[0][0],'1','ten',t_edcl['id'],'0')
        mp(ten_int1)
        print("----------------------")
        print(json.dumps(ten_int1))
        ten_int1 = confLRInts(man,json.dumps(ten_int1),'tier-0s',t_t0_1['id'],'default',auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==', objectId=ten_int1['id'])

        print('**********************************************************')
        print("Tenant T0 - LR Interface 2 Configuration")
        print('**********************************************************')
        ten_int2 = buildLRInterface(tc,pri_ips2[0][0],'2','ten',t_edcl['id'],'1')
        mp(ten_int2)
        print("----------------------")
        print(json.dumps(ten_int2))
        ten_int2 = confLRInts(man,json.dumps(ten_int2),'tier-0s',t_t0_1['id'],'default',auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==', objectId=ten_int2['id'])

        print('**********************************************************')
        print("Tenant T0 BGP Global Configuration")
        print('**********************************************************')
        t_bgp = buildBGP(tc, '','','',tenBGPAS,type='ten')
        mp(t_bgp)
        print("----------------------")
        print(json.dumps(ten_int2))
        t_bgp = confBGP(man, json.dumps(t_bgp),'tier-0s',t_t0_1['id'], auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==', objectId=None)

        print('**********************************************************')
        print("Tenant T0 - BGP Neighbor Configuration 1")
        print('**********************************************************')
        ten_neigh1 = buildBGP(tc, 'neigh', pri_ips1[0][0].split('/')[0],pri_ips1[0][3],proBGPAS,'1','ten')
        mp(ten_neigh1)
        print("----------------------")
        print(json.dumps(ten_neigh1))
        ten_neigh1 = confBGPNeigh(man, json.dumps(ten_neigh1), 'tier-0s', t_t0_1['id'],
                                  'default',auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==', objectId=ten_neigh1['id'])

        print('**********************************************************')
        print("Tenant T0 - BGP Neighbor Configuration 2")
        print('**********************************************************')
        ten_neigh2 = buildBGP(tc, 'neigh', pri_ips2[0][0].split('/')[0],pri_ips2[0][3],proBGPAS,'2','ten')
        mp(ten_neigh2)
        print("----------------------")
        print(json.dumps(ten_neigh2))
        ten_neigh2 = confBGPNeigh(man, json.dumps(ten_neigh2), 'tier-0s', t_t0_1['id'],
                                  'default',auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==', objectId=ten_neigh2['id'])

        print('**********************************************************')
        print("Production - Tenant DHCP Server Configuration")
        print('**********************************************************')
        t_dhcp_svr = buildDHCPServer(tc, 'prod', t_edcl['id'])
        mp(t_dhcp_svr)
        print("----------------------")
        print(json.dumps(t_dhcp_svr))
        t_dhcp_svr = confDHCPSvr(man, json.dumps(t_dhcp_svr), auth=auth_nsx, d_id=t_dhcp_svr['id'])

        print('**********************************************************')
        print("Production - T1 LR Configuration")
        print('**********************************************************')
        t_t1_1 = buildLR(tc, 't1','prod',t_dhcp_svr['id'])
        mp(t_t1_1)
        print("----------------------")
        print(json.dumps(t_t1_1))
        t_t1_1 = confTier1(man, json.dumps(t_t1_1), auth=auth_nsx, objectId=t_t1_1['id'])

        print('**********************************************************')
        print("Production - Tenant T1 LR Local Services Global  Configuration")
        print('**********************************************************')
        print("Building Local-Service...")
        t_locsrv_1 = buildLocServ(tc, t_edcl['id'],'t1')
        mp(t_locsrv_1)
        print("----------------------")
        print(json.dumps(t_locsrv_1))
        t_locsrv_1 = confLocServ(man, json.dumps(t_locsrv_1), t_t1_1['id'],
                                 auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==', objectId='default',mode=1)
        print('**********************************************************')
        print("Production - T1 DNS Server Configuration")
        print('**********************************************************')
        t_dns = buildDNSServer(tc, 'prod')
        mp(t_dns)
        print("----------------------")
        print(json.dumps(t_dns))
        t_dns = confDNSServer(man, json.dumps(t_dns), t_t1_1['id'], auth=auth_nsx)

        print('**********************************************************')
        print("Production - Segment Configuration")
        print('**********************************************************')
        t_prod_seg = buildSegment(tc, 'l3',None,'prod')
        mp(t_prod_seg)
        print("----------------------")
        print(json.dumps(t_prod_seg))
        t_prod_seg = confSegment(man, json.dumps(t_prod_seg), auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==', objectId=t_prod_seg['id'])

        print('**********************************************************')
        print("Production - NAT Configuration")
        print('**********************************************************')
        t_nat_01 = buildNAT(tc,'',nat_ip[0][0].split('/')[0],'192.168.162.0/24','prod-out',t_t0_1['id'])
        t_nat_02 = buildNAT(tc,'',nat_ip[0][0].split('/')[0],'10.1.3.2','prod-dns-out',t_t0_1['id'])
        mp(t_nat_01)
        print("+++++++")
        mp(t_nat_02)
        print("----------------------")
        print(json.dumps(t_nat_01))
        print(json.dumps(t_nat_02))
        db.updAddresses(tc, nat_ip[0][0], 'out-nat')
        t_nat_01 = confNATRules(man, auth_nsx, json.dumps(t_nat_01), objectId=t_t0_1['id'], natRuleId=t_nat_01['id'])
        t_nat_02 = confNATRules(man, auth_nsx, json.dumps(t_nat_02), objectId=t_t0_1['id'], natRuleId=t_nat_02['id'])
        print(' -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*- ')
        print('**********************************************************')
        print("Development - Tenant DHCP Server Configuration")
        print('**********************************************************')
        t_dev_dhcp_svr = buildDHCPServer(tc, 'dev', t_edcl['id'])
        mp(t_dev_dhcp_svr)
        print("----------------------")
        print(json.dumps(t_dev_dhcp_svr))
        t_dev_dhcp_svr = confDHCPSvr(man, json.dumps(t_dev_dhcp_svr), auth=auth_nsx, d_id=t_dev_dhcp_svr['id'])

        print('**********************************************************')
        print("Development - T1 LR Configuration")
        print('**********************************************************')
        t_dev_t1_1 = buildLR(tc, 't1', 'dev', t_dev_dhcp_svr['id'])
        mp(t_dev_t1_1)
        print("----------------------")
        print(json.dumps(t_t1_1))
        t_dev_t1_1 = confTier1(man, json.dumps(t_dev_t1_1), auth=auth_nsx, objectId=t_dev_t1_1['id'])

        print('**********************************************************')
        print("Development - Tenant T1 LR Local Services Global  Configuration")
        print('**********************************************************')
        print("Building Local-Service...")
        t_dev_locsrv_1 = buildLocServ(tc, t_edcl['id'], 't1')
        mp(t_dev_locsrv_1)
        print("----------------------")
        print(json.dumps(t_dev_locsrv_1))
        t_dev_locsrv_1 = confLocServ(man, json.dumps(t_dev_locsrv_1), t_dev_t1_1['id'],
                                 auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==', objectId='default', mode=1)
        print('**********************************************************')
        print("Development - T1 DNS Server Configuration")
        print('**********************************************************')
        t_dev_dns = buildDNSServer(tc, 'dev')
        mp(t_dev_dns)
        print("----------------------")
        print(json.dumps(t_dev_dns))
        t_dns = confDNSServer(man, json.dumps(t_dev_dns), t_dev_t1_1['id'], auth=auth_nsx)

        print('**********************************************************')
        print("Development - Segment Configuration")
        print('**********************************************************')
        t_dev_seg = buildSegment(tc, 'l3', None, 'dev')
        mp(t_dev_seg)
        print("----------------------")
        print(json.dumps(t_dev_seg))
        t_dev__seg = confSegment(man, json.dumps(t_dev_seg), auth='Basic YWRtaW46SVRhYVN3aW5zISFTQUlDMTgxMQ==',
                                 objectId=t_dev_seg['id'])

        print('**********************************************************')
        print("Development - NAT Configuration")
        print('**********************************************************')
        t_dev_nat_01 = buildNAT(tc, '', nat_ip[3][0].split('/')[0], '192.168.163.0/24', 'dev-out', t_t0_1['id'])
        t_dev_nat_02 = buildNAT(tc, '', nat_ip[3][0].split('/')[0], '10.1.4.2', 'dev-dns-out', t_t0_1['id'])
        mp(t_nat_01)
        print("+++++++")
        mp(t_dev_nat_02)
        print("----------------------")
        print(json.dumps(t_dev_nat_01))
        print(json.dumps(t_dev_nat_02))
        db.updAddresses(tc, nat_ip[3][0], 'dev-out-nat')
        t_dev_nat_01 = confNATRules(man, auth_nsx, json.dumps(t_dev_nat_01), objectId=t_t0_1['id'], natRuleId=t_dev_nat_01['id'])
        t_dev_nat_02 = confNATRules(man, auth_nsx, json.dumps(t_dev_nat_02), objectId=t_t0_1['id'], natRuleId=t_dev_nat_02['id'])
        print(' -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*- ')
    en_t = time.time()
    to_t = en_t - st_t
    x=2
    print ("This script took " + str(to_t) + " seconds to run!")
else:
    print("Imported by " + __name__)