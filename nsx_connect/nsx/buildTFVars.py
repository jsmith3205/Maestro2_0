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
    # build+='    default = "'+comp-overlay-tz+'"\n'
    build+='    default = "comp-overlay-tz"\n'
    build+='}\n\n'

    # Need to update code to automatically finde this information
    build+='variable "vlan_tz" {\n'
    # build+='    default = "'+comp-vlan-tz+'"\n'
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
    build+='        name                  = "'+data['meta']['tc']+'TF_Tier0"\n'
    build+='        description           = "'+data['meta']['tc']+'Tier-0 provisioned by Terraform"\n'
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
    build+='            description       = "'+data['meta']['tc']+' T0 interface 1 provisioned by Terraform"\n'
    build+='            int_type          = "EXTERNAL"\n'
    # build+='            gwy_path          = "'+gwy_path+'"\n'
    build+='            seg_path          = "/infra/segments/'+data['segments']['up1']+'"\n'
    build+='            subnets           = ["'+data['ip']['tran1']+'"]\n'  # This will become the pri_ips1[0][0]
    build+='            mtu               = 1500\n'
    build+='        },{\n'
    build+='            name              = "to-provider-02"\n'
    build+='            description       = "'+data['meta']['tc']+' interface 2 provisioned by Terraform"\n'
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
    build+='        description               = "'+data['meta']['tc']+' Tier1 provisioned by Terraform"\n'
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
    build+='        description               = "'+data['meta']['tc']+' Tier1 provisioned by Terraform"\n'
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
            name = string
            description = string
            server_address = string
            dhcp_range = list(string)
    }))\n'''

    build+='    default = [{\n'
    build+='    name = "okr01-c01-'+data['meta']['tc']+'seg-prod"\n'
    build+='    description = "'+data['meta']['tc'].capitalize()+' production segment deployment using Terraform"\n'
    build+='    server_address = "192.168.162.5/24"\n'
    build+='    dhcp_range = ["192.168.165.32-192.168.165.254"]\n'
    build+='},{\n'
    build+='    name = "okr01-c01-'+data['meta']['tc']+'seg-dev"\n'
    build+='    description = "'+data['meta']['tc'].capitalize()+' production segment deployment using Terraform"\n'
    build+='    server_address = "192.168.162.5/24"\n'
    build+='    dhcp_range = ["192.168.165.32-192.168.165.254"]\n'
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
    build+='    description = "'+data['meta']['tc']+' DHCP server deployment using Terraform"\n'
    build+='    server_address = ["10.1.1.2/24"]\n'
    build+='}]\n'
    build+='}\n'
    return build
