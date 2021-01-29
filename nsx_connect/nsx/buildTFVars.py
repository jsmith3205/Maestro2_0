#!/usr/bin/python3


def buildTFVars(data):
    build = "# Variables\n\n"

    build +="# NSX Manager - Be sure to change based on your environment\n"
    build +='variable "nsx_manager" {\n'
    build +='    default = "'+data['conn']['nman']+'"\n'
    build +="}\n\n"

    build+="# Username & Password for NSX-T Manager\n"
    build+='variable "username" {\n'
    build+='    default = "'+data['conn']['nu']+'"\n'
    build+='}\n\n'

    build+='variable "password" {\n'
    build+='    default = "'+data['conn']['np']+'"\n'
    build+='}\n\n'

    # Need to update code to automatically finde this information
    build+='# Transport Zones\n'
    build+='variable "overlay_tz" {\n'
    build+='    default = "comp-overlay-tz"\n'
    build+='}\n\n'

    # Need to update code to automatically finde this information
    build+='variable "vlan_tz" {\n'
    build+='    default = "comp-vlan-tz"\n'
    build+='}\n\n'

    build+='# Edge information used for logical routing\n'
    build+='variable "edge_node1" {\n'
    build+='    default = "'+data['edge1']['display_name']+'"\n'
    build+='}\n\n'

    build+='variable "edge_node2" {\n'
    build+='    default = "'+data['edge2']['display_name']+'"\n'
    build+='}\n\n'

    build+='variable "edge_cluster" {\n'
    build+='    default = "'+data['edcl']['display_name']+'"\n'
    build+='}\n\n'

    build+='''variable "t_t0" {
        type                        = list(object({
            name                    = string
            description             = string
            failover_mode           = string
            default_rule_logging    = bool
            enable_firewall         = bool
            force_whitelisting      = bool
            ha_mode                 = string
            edge_cluster_path       = string
            bgp_config              = object({
                ecmp                = bool
                local_as_num        = string
                multipath_relax     = bool

            })
            interfaces              = list(object({
                name                = string
                description         = string
                int_type            = string
                seg_path            = string
                subnets             = list(string)
                mtu                 = number
            }))
        }))\n'''

    build+='    default = [{\n'
    build+='        name                  = "okr01-c01-'+data['meta']['tc']+'-t0"\n'
    build+='        description           = "'+data['meta']['tc'].capitalize()+' Tier-0 provisioned by Terraform"\n'
    build+='        failover_mode         = "NON_PREEMPTIVE"\n'
    build+='        default_rule_logging  = false\n'
    build+='        enable_firewall       = false\n'
    build+='        force_whitelisting    = true\n'
    build+='        ha_mode               = "ACTIVE_STANDBY"\n'
    build+='        edge_cluster_path     = "'+data['edcl']['edcl_path']+'"\n'
    build+='        bgp_config            = {\n'
    build+='            ecmp              = false\n'
    build+='            local_as_num      = "'+data['ip']['bgpas']+'"\n'
    build+='            multipath_relax   = false\n'
    build+='        }\n'
    build+='        interfaces            = [{\n'
    build+='            name              = "to-provider-01"\n'
    build+='            description       = "'+data['meta']['tc'].capitalize()+' T0 interface 1 provisioned by Terraform"\n'
    build+='            int_type          = "EXTERNAL"\n'
    # build+='            gwy_path          = "'+gwy_path+'"\n'
    build+='            seg_path          = "/infra/segments/'+data['segments']['up1']+'"\n'
    build+='            subnets           = ["'+data['ip']['tran1']+'"]\n'  # This will become the pri_ips1[0][0]
    build+='            mtu               = 1500\n'
    build+='        },{\n'
    build+='            name              = "to-provider-02"\n'
    build+='            description       = "'+data['meta']['tc'].capitalize()+' interface 2 provisioned by Terraform"\n'
    build+='            int_type          = "EXTERNAL"\n'
    # build+='            gwy_path          = "'+gwy_path+'"\n'
    build+='            seg_path          = "/infra/segments/'+data['segments']['up2']+'"\n'
    build+='            subnets           = ["'+data['ip']['tran2']+'"]\n'  # This will become the pri_ips2[0][0]
    build+='            mtu               = 1500\n'
    build+='        }]\n'
    build+='    }]\n'
    build+='}\n\n'

    build+='''variable "t_t1" {
        type                            = list(object({
            name                        = string
            description                 = string
            failover_mode               = string
            default_rule_logging        = bool
            enable_firewall             = bool
            force_whitelisting          = bool
            edge_cluster_path           = string
            enable_standby_relocation   = string
            route_advertisement_types   = list(string)
            pool_allocation             = string
        }))\n\n'''

    build+='    default = [{\n'
    build+='        name              = "okr01-c01-'+data['meta']['tc']+'-t1-prod"\n'
    build+='        description               = "'+data['meta']['tc'].capitalize()+' Tier1 provisioned by Terraform"\n'
    build+='        edge_cluster_path         = "'+data['edcl']['edcl_path']+'"\n'
    # build+='        dhcp_config_path          = "'+dhcp_path+'\n"'
    build+='        failover_mode             = "PREEMPTIVE"\n'
    build+='        default_rule_logging      = false\n'
    build+='        enable_firewall           = true\n'
    build+='        enable_standby_relocation = false\n'
    build+='        force_whitelisting        = false\n'
 #   build+='        tier0_path                = "'+t0_path+'\n"'
    build+='        route_advertisement_types = ["TIER1_CONNECTED"]\n'
    build+='        pool_allocation           = "ROUTING"\n'
    build+='        },{\n'
    build+='        name              = "okr01-c01-'+data['meta']['tc']+'-t1-dev"\n'
    build+='        description               = "'+data['meta']['tc'].capitalize()+' Tier1 provisioned by Terraform"\n'
    build+='        edge_cluster_path         = "'+data['edcl']['edcl_path']+'"\n'
    # build+='        dhcp_config_path          = "'+dhcp_path+'"\n'
    build+='        failover_mode             = "PREEMPTIVE"\n'
    build+='        default_rule_logging      = false\n'
    build+='        enable_firewall           = true\n'
    build+='        enable_standby_relocation = false\n'
    build+='        force_whitelisting        = false\n'
 #   build+='        tier0_path                = "'+t0_path+'\n"'
    build+='        route_advertisement_types = ["TIER1_CONNECTED"]\n'
    build+='        pool_allocation           = "ROUTING"\n'
    build+='    }]\n'
    build+='}\n'

    build+='''# Segment Names
    variable "segments" {
        type = list(object({
            name            = string
            description     = string
            server_address  = string
            dhcp_range      = list(string)
            cidr            = string
    }))\n'''

    build+='    default         = [{\n'
    build+='    name            = "okr01-c01-'+data['meta']['tc']+'-seg-prod"\n'
    build+='    description     = "'+data['meta']['tc'].capitalize()+' production segment deployment using Terraform"\n'
    build+='    server_address  = "192.168.162.5/24"\n'
    build+='    dhcp_range      = ["192.168.162.32-192.168.162.254"]\n'
    build+='    cidr            = "192.168.162.1/24"\n'
    build+='},{\n'
    build+='    name            = "okr01-c01-'+data['meta']['tc']+'-seg-dev"\n'
    build+='    description     = "'+data['meta']['tc'].capitalize()+' development segment deployment using Terraform"\n'
    build+='    server_address  = "192.168.163.5/24"\n'
    build+='    dhcp_range      = ["192.168.163.32-192.168.163.254"]\n'
    build+='    cidr            = "192.168.163.1/24"\n'
    build+='}]\n'
    build+='}\n'
    build+='''variable "dhcp_server" {
            type = list(object({
            name = string
            description = string
            server_address = list(string)
            }))\n'''
    build+='    default= [{\n'
    build+='    name = "okr01-c01-'+data['meta']['tc']+'-dhcpd"\n'
    build+='    description = "'+data['meta']['tc'].capitalize()+' DHCP server deployment using Terraform"\n'
    build+='    server_address = ["10.1.1.2/24"]\n'
    build+='}]\n'
    build+='}\n'
    
    build+='''# NAT Policies
    variable "nat" {
        type = list(object({
            name            = string
            description     = string
            action          = string
            s_nets          = list(string)
            d_nets          = list(string)
            t_nets          = list(string)
            gw_path         = string
            logging         = bool
            fw_match        = string
    }))\n'''
    build+='    default= [{\n'
    build+='    name = "' + data['meta']['tc']+'-out"\n'
    build+='    description = "'+data['meta']['tc'].capitalize()+' NAT Deployment using Terraform"\n'
    build+='    action = "SNAT"\n'
    build+='    s_nets = ["'+data['ip']['d_net']+'","'+data['ip']['p_net']+'" ]\n'
    build+='    d_nets = ["ANY"]\n'
    build+='    t_nets = ["'+data['ip']['nat1']+'"]\n'
    build+='    gw_path = ""\n'
    build+='    logging = false\n'
    build+='    fw_match = "MATCH_EXTERNAL_ADDRESS"\n'
    build+='},{\n'
    build+='    name = "' + data['meta']['tc']+'-rds-in"\n'
    build+='    description = "'+data['meta']['tc'].capitalize()+' NAT Deployment using Terraform"\n'
    build+='    action = "DNAT"\n'
    build+='    s_nets = ["ANY" ]\n'
    build+='    d_nets = ["'+data['ip']['p_lan_ip1']+'"]\n'
    build+='    t_nets = ["'+data['ip']['nat2']+'"]\n'
    build+='    gw_path = ""\n'
    build+='    logging = false\n'
    build+='    fw_match = "MATCH_EXTERNAL_ADDRESS"\n'
    build+='},{\n'
    build+='    name = "' + data['meta']['tc']+'-oc-in"\n'
    build+='    description = "'+data['meta']['tc'].capitalize()+' NAT Deployment using Terraform"\n'
    build+='    action = "DNAT"\n'
    build+='    s_nets = ["ANY" ]\n'
    build+='    d_nets = ["'+data['ip']['p_lan_ip2']+'"]\n'
    build+='    t_nets = ["'+data['ip']['nat3']+'"]\n'
    build+='    gw_path = ""\n'
    build+='    logging = false\n'
    build+='    fw_match = "MATCH_EXTERNAL_ADDRESS"\n'
    build+='}]\n'
    build+='}\n'

    build+='# BGP Neighbor\n'
    build+='variable "bgp_neighbor" {\n'
    build+='type = list(object({\n'
    build+='        name              = string\n'
    build+='        description       = string\n'
    build+='        bgp_path          = string\n'
    build+='        allow_as_in       = bool\n'
    build+='        gr_mode           = string\n'
    build+='        hd_time           = number\n'
    build+='        ka_time           = number\n'
    build+='        n_addr            = string\n'
    build+='        pass              = string\n'
    build+='        rem_as            = string\n'
    build+='        s_address         = string\n'
    build+='}))\n'
    build+='default = [{\n'
    build+='name                = "To-'+data['meta']['tc'].capitalize()+'-01"\n'
    build+='description         = "To '+data['meta']['tc'].capitalize()+' 1"\n'
    build+='bgp_path            = ""\n'
    build+='allow_as_in         = false\n'
    build+='gr_mode             = "HELPER_ONLY"\n'
    build+='hd_time             = 300\n'
    build+='ka_time             = 100\n'
    build+='n_addr    = "'+data['ip']['tran1'].split('/')[0]+'"\n'
    build+='pass            = ""\n'
    build+='rem_as       = "65064"\n'
    build+='s_address      = ""\n'
    build+='},{\n'
    build+='name                = "To-'+data['meta']['tc'].capitalize()+'-02"\n'
    build+='description         = "To '+data['meta']['tc'].capitalize()+' 2"\n'
    build+='bgp_path            = ""\n'
    build+='allow_as_in         = false\n'
    build+='gr_mode             = "HELPER_ONLY"\n'
    build+='hd_time             = 100\n'
    build+='ka_time             = 300\n'
    build+='n_addr    = "'+data['ip']['tran2'].split('/')[0]+'"\n'
    build+='pass            = ""\n'
    build+='rem_as       = "65064"\n'
    build+='s_address      = ""\n'
    build+='},{\n'
    build+='name                = "To-Provider-01"\n'
    build+='description         = "To Provider 01"\n'
    build+='bgp_path            = ""\n'
    build+='allow_as_in         = false\n'
    build+='gr_mode             = "HELPER_ONLY"\n'
    build+='hd_time             = 300\n'
    build+='ka_time             = 100\n'
    build+='n_addr    = "192.168.164.1"\n'
    build+='pass            = ""\n'
    build+='rem_as       = "65000"\n'
    build+='s_address      = ""\n'
    build+='},{\n'
    build+='name                = "To-Provider-02"\n'
    build+='description         = "To Provider 02"\n'
    build+='bgp_path            = ""\n'
    build+='allow_as_in         = false\n'
    build+='gr_mode             = "HELPER_ONLY"\n'
    build+='hd_time             = 300\n'
    build+='ka_time             = 100\n'
    build+='n_addr    = "192.168.165.1"\n'
    build+='pass            = ""\n'
    build+='rem_as       = "65000"\n'
    build+='s_address      = ""\n'
    build+='}]\n'
    build+='}\n'

    # DNS Services
    build+='variable "dns_zone" {\n'
    build+='    type = list(object({\n'
    build+='                name = string\n'
    build+='                description  = string\n'
    build+='                servers = list(string)\n'
    build+='            }))\n'
    build+='    default= [{\n'
    build+='        name        = "okr01-c01-test5-dns-zone"\n'
    build+='        description = "Test5 DNS forwarder deployment using Terraform"\n'
    build+='        servers     = ["172.16.11.11","172.16.11.12"]\n'
    build+='    }]\n'
    build+='}\n'

    build+='variable "dns_forwarder" {\n'
    build+='    type = list(object({\n'
    build+='                name = string\n'
    build+='                listener_ip  = string\n'
    build+='                description  = string\n'
    build+='                enabled = bool\n'
    build+='                log_level = string\n'
    build+='            }))\n'
    build+='    default= [{\n'
    build+='        name        = "okr01-c01-test5-dns-forwarder"\n'
    build+='        description = "Test5 DNS forwarder deployment using Terraform"\n'
    build+='        listener_ip = "10.1.1.2"\n'
    build+='        enabled     = true\n'
    build+='        log_level   = "DEBUG"\n'
    build+='    }]\n'
    build+='}\n'

    return build
