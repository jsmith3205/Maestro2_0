# Variables

# NSX Manager - Be sure to change based on your environment
variable "nsx_manager" {
    default = "172.16.11.30"
}

# Username & Password for NSX-T Manager
variable "username" {
    default = "admin"
}

variable "password" {
    default = "ITaaSwins!!SAIC1811"
}

# Transport Zones
variable "overlay_tz" {
    default = "comp-overlay-tz"
}

variable "vlan_tz" {
    default = "comp-vlan-tz"
}

# Edge information used for logical routing
variable "edge_node1" {
    default = "okr01-c01-pytf04-01"
}

variable "edge_node2" {
    default = "okr01-c01-pytf04-02"
}

variable "edge_cluster" {
    default = "okr01-c01-pytf04-01"
}

variable "t_t0" {
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
        }))
    default = [{
        name                  = "pytf04TF_Tier0"
        description           = "pytf04Tier-0 provisioned by Terraform"
        failover_mode         = "NON_PREEMPTIVE"
        default_rule_logging  = false
        enable_firewall       = false
        force_whitelisting    = true
        ha_mode               = "ACTIVE_STANDBY"
        edge_cluster_path     = "/infra/sites/default/enforcement-points/default/edge-clusters/6a12b978-54a8-4c69-9279-b5f77708cbc9"
        bgp_config            = {
            ecmp              = false
            local_as_num      = "65102"
            multipath_relax   = false
        }
        interfaces            = [{
            name              = "to-provider-01"
            description       = "pytf04 T0 interface 1 provisioned by Terraform"
            int_type          = "EXTERNAL"
            seg_path          = "/infra/segments/okr01-c01-tenant-uplinks"
            subnets           = ["192.168.164.54/24"]
            mtu               = 1500
        },{
            name              = "to-provider-02"
            description       = "pytf04 interface 2 provisioned by Terraform"
            int_type          = "EXTERNAL"
            seg_path          = "/infra/segments/okr01-c01-tenant-uplink02"
            subnets           = ["192.168.165.54/24"]
            mtu               = 1500
        }]
    }]
}

variable "t_t1" {
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
        }))

    default = [{
        name              = "okr01-c01-pytf04-t1-prod"
        description               = "pytf04 Tier1 provisioned by Terraform"
        edge_cluster_path         = "/infra/sites/default/enforcement-points/default/edge-clusters/6a12b978-54a8-4c69-9279-b5f77708cbc9"
        failover_mode             = "PREEMPTIVE"
        default_rule_logging      = false
        enable_firewall           = true
        enable_standby_relocation = false
        force_whitelisting        = false
        route_advertisement_types = ["TIER1_CONNECTED"]
        pool_allocation           = "ROUTING"
        },{
        name              = "okr01-c01-pytf04-t1-dev"
        description               = "pytf04 Tier1 provisioned by Terraform"
        edge_cluster_path         = "/infra/sites/default/enforcement-points/default/edge-clusters/6a12b978-54a8-4c69-9279-b5f77708cbc9"
        failover_mode             = "PREEMPTIVE"
        default_rule_logging      = false
        enable_firewall           = true
        enable_standby_relocation = false
        force_whitelisting        = false
        route_advertisement_types = ["TIER1_CONNECTED"]
        pool_allocation           = "ROUTING"
    }]
}
# Segment Names
    variable "segments" {
        type = list(object({
            name = string
            description = string
            server_address = string
            dhcp_range = list(string)
            subnet = string
    }))
    default = [{
    name = "okr01-c01-pytf04seg-prod"
    description = "Test production segment deployment using Terraform"
    server_address = "192.168.162.5/24"
    dhcp_range = ["192.168.162.32-192.168.162.254"]
    subnet = "192.168.162.1/24"
},{
    name = "okr01-c01-pytf04seg-dev"
    description = "Test production segment deployment using Terraform"
    server_address = "192.168.163.5/24"
    dhcp_range = ["192.168.163.32-192.168.163.254"]
    subnet = "192.168.163.1/24"
}]
}
variable "dhcp_server" {
            type = list(object({
            name = string
            description = string
            server_address = list(string)
            }))
    default= [{
    name = "okr01-c01-pytf04-dhcpd"
    description = "pytf04 DHCP server deployment using Terraform"
    server_address = ["10.1.1.2/24"]
}]
}