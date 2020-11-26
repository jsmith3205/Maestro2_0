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
    default = ""
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
    default = "TF-TEST01-sdn-edge01" # this will need to be the json display_name
}

variable "edge_node2" {
    default = "TF-TEST01-sdn-edge02" # this will need to be the json display_name
}

variable "edge_cluster" {
    default = "TF-TEST01-tenant-edcl01" # this will need to change to the json display_name
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
            gwy_path            = string
            seg_path            = string
            subnets             = list(string)
            mtu                 = number
        }))
    }))

    default = [{
        name                  = "TF_Tier0"
        description           = "Tenant Tier-0 provisioned by Terraform"
        failover_mode         = "NON_PREEMPTIVE"
        default_rule_logging  = false
        enable_firewall       = false
        force_whitelisting    = true
        ha_mode               = "ACTIVE_STANDBY"
        edge_cluster_path     = ""
        bgp_config            = {
            ecmp              = false
            local_as_num      = "65065"
            multipath_relax   = false
        }
        interfaces            = [{
            name              = "to-provider-01"
            description       = "Tenant T0 interface 1 provisioned by Terraform"
            int_type          = "EXTERNAL"
            gwy_path          = ""
            seg_path          = "/infra/segments/okr01-c01-tenant-uplinks"
            subnets           = ["192.168.164.23/24"]  # This will become the pri_ips1[0][0]
            mtu               = 1500
        },
        {
            name              = "to-provider-02"
            description       = "Tenant T0 interface 2 provisioned by Terraform"
            int_type          = "EXTERNAL"
            gwy_path          = ""
            seg_path          = "/infra/segments/okr01-c01-tenant-uplink02"
            subnets           = ["192.168.165.23/24"]  # This will become the pri_ips2[0][0]
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
        dhcp_config_path            = string
        enable_standby_relocation   = string
        tier0_path                  = string
        route_advertisement_types   = list(string)
        pool_allocation             = string
    }))

    default = [{
        name              = "TF_T1_prod"
        description               = "Tier1 provisioned by Terraform"
        edge_cluster_path         = ""
        dhcp_config_path          = ""
        failover_mode             = "PREEMPTIVE"
        default_rule_logging      = false
        enable_firewall           = true
        enable_standby_relocation = false
        force_whitelisting        = false
        tier0_path                = ""
        route_advertisement_types = ["TIER1_CONNECTED"]
        pool_allocation           = "ROUTING"
    }]
}

# Segment Names
variable "segments" {
    type = list(object({
        name = string
        description = string
        subnet = string
  }))
  default = [{
      name = "tf-test-production"
      description = "Test production segment deployment using Terraform"
      subnet = "192.168.162.1/24"
  },
  {
      name = "tf-test-development"
      description = "Test production segment deployment using Terraform"
      subnet = "192.168.163.1/24"
  }]
}
variable "dhcp_server" {
  type = list(object({
      name = string
      description = string
      server_address = list(string)
  }))
  default=[{
     name = "tf-test-dhcp"
     description = "Test DHCP server deployment using Terraform"
     server_address = ["10.1.1.2/24"]
  }]
}  