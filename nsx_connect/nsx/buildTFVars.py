def buildTFVars(man='',user='',my_pass='',ov_tz='',vl_tz='',en1='',en2='',ec='',):
    build = 
    build = "# Variables"

    build +="# NSX Manager - Be sure to change based on your environment"
    build +='variable "nsx_manager" {'
    build +='    default = "'+172.16.11.30+'"'
    build +="}"

    build+="# Username & Password for NSX-T Manager"
    build+='variable "username" {'
    build+='    default = "'+admin+'"'
    build+='}'

    build+='variable "password" {'
    build+='    default = "'+my_pass+'"'
    build+='}'

    build+='# Transport Zones'
    build+='variable "overlay_tz" {'
    build+='    default = "'+comp-overlay-tz+'"'
    build+='}'

    build+='variable "vlan_tz" {'
    build+='    default = "'+comp-vlan-tz+'"'
    build+='}'

    build+='# Edge information used for logical routing'
    build+='variable "edge_node1" {'
    build+='    default = "'+TF-TEST01-sdn-edge01+'"' # this will need to be the json display_name
    build+='}'

    build+='variable "edge_node2" {'
    build+='    default = "'+TF-TEST01-sdn-edge02+'"' # this will need to be the json display_name
    build+=}

    build+='variable "edge_cluster" {'
    build+='    default = "'+TF-TEST01-tenant-edcl01+'"' # this will need to change to the json display_name
    build+='}'

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
                gwy_path            = string
                seg_path            = string
                subnets             = list(string)
                mtu                 = number
            }))
        }))'''

    build+='    default = [{'
    build+='        name                  = '"+TF_Tier0+'"'
    build+='        description           = "Tenant Tier-0 provisioned by Terraform"'
    build+='        failover_mode         = "NON_PREEMPTIVE"'
    build+='        default_rule_logging  = false'
    build+='        enable_firewall       = false'
    build+='        force_whitelisting    = true'
    build+='        ha_mode               = "ACTIVE_STANDBY"'
    build+='        edge_cluster_path     = "'+ec+''"'
    build+='        bgp_config            = {'
    build+='            ecmp              = false'
    build+='            local_as_num      = "'+65065+'"'
    build+='            multipath_relax   = false'
    build+='        }'
    build+='        interfaces            = [{'
    build+='            name              = "'+to-provider-01+'"'
    build+='            description       = "Tenant T0 interface 1 provisioned by Terraform"'
    build+='            int_type          = "EXTERNAL"'
    build+='            gwy_path          = "'+gwy_path+'"'
    build+='            seg_path          = "'+/infra/segments/okr01-c01-tenant-uplinks+'"'
    build+='            subnets           = '+["192.168.164.23/24"]  # This will become the pri_ips1[0][0]
    build+='            mtu               = 1500'
    build+='        },{'
    build+='            name              = "to-provider-02"'
    build+='            description       = "Tenant T0 interface 2 provisioned by Terraform"'
    build+='            int_type          = "EXTERNAL"'
    build+='            gwy_path          = "'+gwy_path+'"'
    build+='            seg_path          = "'+/infra/segments/okr01-c01-tenant-uplink02+'"'
    build+='            subnets           = '+["192.168.165.23/24"]  # This will become the pri_ips2[0][0]
    build+='            mtu               = 1500'
    build+='        }]'
    build+='    }]'
    build+='}'

    build+='''variable "t_t1" {
        type                            = list(object({
            name                        = string
            description                 = string
            failover_mode               = string
            default_rule_logging        = bool
            enable_firewall             = bool
            force_whitelisting          = bool
            edge_cluster_path           = string
            dhcp_config_path            = string
            enable_standby_relocation   = string
            tier0_path                  = string
            route_advertisement_types   = list(string)
            pool_allocation             = string
        }))'''

    build+='    default = [{'
    build+='        name              = "'+TF_T1_prod+'"'
    build+='        description               = "Tier1 provisioned by Terraform"'
    build+='        edge_cluster_path         = "'+ec_path+'"'
    build+='        dhcp_config_path          = "'+dhcp_path+'"'
    build+='        failover_mode             = "'+PREEMPTIVE+'"'
    build+='        default_rule_logging      = false'
    build+='        enable_firewall           = true'
    build+='        enable_standby_relocation = false'
    build+='        force_whitelisting        = false'
    build+='        tier0_path                = "'+t0_path+'"'
    build+='        route_advertisement_types = ["TIER1_CONNECTED"]'
    build+='        pool_allocation           = "ROUTING"'
    build+='    }]'
    build+='}'

    build+='''# Segment Names
    variable "segments" {
        type = list(object({
            name = string
            description = string
            subnet = string
    }))'''

    build+='default = [{'
    build+='    name = "'+tf-test-production+'"'
    build+='    description = "Test production segment deployment using Terraform"'
    build+='    subnet = "'+192.168.162.1/24+'"'
    build+='},{'
    build+='    name = "'+tf-test-development+'"'
    build+='    description = "Test production segment deployment using Terraform"'
    build+='    subnet = "'+192.168.163.1/24+'"'
    build+='}]'
    build+='}'
    build+='''variable "dhcp_server" {
    type = list(object({
        name = string
        description = string
        server_address = list(string)
    }))'''
    build+=default='[{'
    build+='    name = "'+tf-test-dhcpd+'"'
    build+='    description = "Test DHCP server deployment using Terraform"'
    build+='    server_address = '+["10.1.1.2/24"]
    build+='}]'
    build+='}'
    
}