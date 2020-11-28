provider "nsxt" {
  host                  = var.nsx_manager
  username              = var.username
  password              = var.password
  allow_unverified_ssl  = true
  max_retries           = 10
  retry_min_delay       = 500
  retry_max_delay       = 5000
  retry_on_status_codes = [429]
}

data "nsxt_policy_edge_node" "node1" {
  edge_cluster_path = data.nsxt_policy_edge_cluster.edge_cluster.path
  display_name = var.edge_node1
}

data "nsxt_policy_edge_node" "node2" {
  edge_cluster_path = data.nsxt_policy_edge_cluster.edge_cluster.path  
  display_name = var.edge_node2
}

data "nsxt_policy_edge_cluster" "edge_cluster" {
  display_name = var.edge_cluster
}

data "nsxt_policy_transport_zone" "overlay_tz" {
  display_name = var.overlay_tz
}

data "nsxt_policy_transport_zone" "vlan_tz" {
  display_name = var.vlan_tz
}

# used for testing now, but will need to be updated for Tenant specific deployments
data "nsxt_policy_tier0_gateway" "t0_gateway" {
  display_name = "okr01-c01-jks02-t0"
}


# Create Tenant DHCP servers for Segments
resource "nsxt_policy_dhcp_server" "t_dhcp" {
  display_name = var.dhcp_server[0].name
  description = var.dhcp_server[0].description
  edge_cluster_path = data.nsxt_policy_edge_cluster.edge_cluster.path
  server_addresses = var.dhcp_server.server_address
}


# Create Tenant Tier-0
resource "nsxt_policy_tier0_gateway" "t_t0" {
  display_name          = var.t_t0.name
  description           = var.t_t0.description
  failover_mode         = var.t_t0.failover_mode
  default_rule_logging  = var.t_t0.default_rule_logging
  enable_firewall       = var.t_t0.enable_firewall
  force_whitelisting    = var.t_t0.force_whitelisting
  ha_mode               = var.t_t0.ha_mode
  edge_cluster_path     = data.nsxt_policy_edge_cluster.edge_cluster.path

  bgp_config {
    ecmp                = var.t_t0.bgp_config.ecmp
    local_as_num        = var.t_t0.bgp_config.local_as_num
    multipath_relax     = var.t_t0.bgp_config.multipath_relax
  }
  # add tags later

}


# Create Tier0 Interfaces
resource "nsxt_policy_tier0_gateway_interface" "t_t0_int1" {
  display_name            = var.t_t0[0].interfaces[0].name
  description             = var.t_t0[0].interfaces[0].description
  type                    = var.t_t0[0].interfaces[0].int_type
  gateway_path            = nsxt_policy_tier0_gateway.t_t0.path
  segment_path            = var.t_t0[0].interfaces[0].seg_path
  subnets                 = var.t_t0[0].interfaces[0].subnets
  mtu                     = var.t_t0[0].interfaces[0].mtu
  edge_node_path          = data.nsxt_policy_edge_node.node1.path
}

resource "nsxt_policy_tier0_gateway_interface" "t_t0_int2" {
  display_name            = var.t_t0[0].interfaces[1].name
  description             = var.t_t0[0].interfaces[1].description
  type                    = var.t_t0[0].interfaces[1].int_type
  gateway_path            = nsxt_policy_tier0_gateway.t_t0.path
  segment_path            = var.t_t0[0].interfaces[1].seg_path
  subnets                 = var.t_t0[0].interfaces[1].subnets
  mtu                     = var.t_t0[0].interfaces[1].mtu
  edge_node_path          = data.nsxt_policy_edge_node.node2.path
}

# Create Tenant Tier-1s
resource "nsxt_policy_tier1_gateway" "t1_prod" {
  display_name              = var.t_t1[0].name
  description               = var.t_t1[0].description
  edge_cluster_path         = data.nsxt_policy_edge_cluster.edge_cluster.path
  dhcp_config_path          = nsxt_policy_dhcp_server.t_dhcp.path
  failover_mode             = var.t_t1[0].failover_mode
  default_rule_logging      = var.t_t1[0].default_rule_logging
  enable_firewall           = var.t_t1[0].enable_firewall
  enable_standby_relocation = var.t_t1[0].enable_standby_relocation
  force_whitelisting        = var.t_t1[0].force_whitelisting
  tier0_path                = nsxt_policy_tier0_gateway.t_t0.path
  route_advertisement_types = var.t_t1[0].route_advertisement_types
  pool_allocation           = "ROUTING"
}

resource "nsxt_policy_tier1_gateway" "t1_dev" {
  display_name              = var.t_t1[1].name
  description               = var.t_t1[1].description
  edge_cluster_path         = data.nsxt_policy_edge_cluster.edge_cluster.path
  dhcp_config_path          = nsxt_policy_dhcp_server.t_dhcp.path
  failover_mode             = var.t_t1[1].failover_mode
  default_rule_logging      = var.t_t1[0].default_rule_logging
  enable_firewall           = var.t_t1[0].enable_firewall
  enable_standby_relocation = var.t_t1[0].enable_standby_relocation
  force_whitelisting        = var.t_t1[0].force_whitelisting
  tier0_path                = nsxt_policy_tier0_gateway.t_t0.path
  route_advertisement_types = var.t_t1[1].route_advertisement_types
  pool_allocation           = "ROUTING"
}

# Create Tenant Segments
resource "nsxt_policy_segment" "prod" {
  display_name        = var.segments[0].name
  description         = var.segments[0].description
  transport_zone_path = data.nsxt_policy_transport_zone.overlay_tz.path
  connectivity_path   = nsxt_policy_tier1_gateway.t1_prod.path

  subnet {
    cidr              = var.segments[0].subnet
    dhcp_ranges       = var.segments[0].dhcp_range

    dhcp_v4_config {
      server_address  = var.segments[0].server_address
    }  
  }

  tag {
    scope = "tier"
    tag   = "prod"
  }
}

resource "nsxt_policy_segment" "dev" {
  display_name        = var.segments[1].name
  description         = var.segments[1].description
  transport_zone_path = data.nsxt_policy_transport_zone.overlay_tz.path
  connectivity_path   = nsxt_policy_tier1_gateway.t1_dev.path

  subnet {
    cidr              = var.segments[1].subnet
    dhcp_ranges       = var.segments[1].dhcp_range

    dhcp_v4_config {
      server_address  = var.segments[1].server_address
    }  
  }

  tag {
    scope = "tier"
    tag   = "dev"
  }
}






# resource "nsxt_policy_segment" "web" {
#   display_name        = "web-tier"
#   description         = "Terraform provisioned Web Segment"
#   connectivity_path   = nsxt_policy_tier1_gateway.t1_gateway.path
#   transport_zone_path = data.nsxt_policy_transport_zone.overlay_tz.path

#   subnet {
#     cidr        = "12.12.1.1/24"
#     dhcp_ranges = ["12.12.1.100-12.12.1.160"]

#     dhcp_v4_config {
#       server_address = "12.12.1.2/24"
#       lease_time     = 36000

#       dhcp_option_121 {
#         network  = "6.6.6.0/24"
#         next_hop = "1.1.1.21"
#       }
#     }
#   }

#   tag {
#     scope = var.nsx_tag_scope
#     tag   = var.nsx_tag
#   }
#   tag {
#     scope = "tier"
#     tag   = "web"
#   }
# }

# resource "nsxt_policy_segment" "app" {
#   display_name        = "app-tier"
#   description         = "Terraform provisioned App Segment"
#   connectivity_path   = nsxt_policy_tier1_gateway.t1_gateway.path
#   transport_zone_path = data.nsxt_policy_transport_zone.overlay_tz.path

#   subnet {
#     cidr        = "12.12.2.1/24"
#     dhcp_ranges = ["12.12.2.100-12.12.2.160"]

#     dhcp_v4_config {
#       server_address = "12.12.2.2/24"
#       lease_time     = 36000

#       dhcp_option_121 {
#         network  = "6.6.6.0/24"
#         next_hop = "1.1.1.21"
#       }
#     }
#   }

#   tag {
#     scope = var.nsx_tag_scope
#     tag   = var.nsx_tag
#   }
#   tag {
#     scope = "tier"
#     tag   = "app"
#   }
# }

# resource "nsxt_policy_segment" "db" {
#   display_name        = "db-tier"
#   description         = "Terraform provisioned DB Segment"
#   connectivity_path   = nsxt_policy_tier1_gateway.t1_gateway.path
#   transport_zone_path = data.nsxt_policy_transport_zone.overlay_tz.path

#   subnet {
#     cidr        = "12.12.3.1/24"
#     dhcp_ranges = ["12.12.3.100-12.12.3.160"]

#     dhcp_v4_config {
#       server_address = "12.12.3.2/24"
#       lease_time     = 36000

#       dhcp_option_121 {
#         network  = "6.6.6.0/24"
#         next_hop = "1.1.1.21"
#       }
#     }
#   }

#   tag {
#     scope = var.nsx_tag_scope
#     tag   = var.nsx_tag
#   }
#   tag {
#     scope = "tier"
#     tag   = "db"
#   }
#}
