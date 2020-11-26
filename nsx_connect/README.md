# nsx_connect
NSX-T program to deploy Tenant Enclaves in a Dual T0 deployment via the NSX-T 2.5 API.

**How does it work?**
This script configures the tenants enclave starting by pulling available IPs from 'ipam.db' file.  The IPs pulled are:
1.  Tenant T0 to Provider T0 IPs.
2.  Public IPs (for NAT and VPN services).
3.  Reusing LAN IPs...no need to pull these.

Once IPs have been gathered and assigned, the workflow is:
1.  Configure Tenant T0 IPs on Provider T0.
2.  Deploy Tenant Edge Nodes (x2)
3.  Deploy Tenant Edge Cluster
4.  Deploy Tenant T0 Logical Router
5.  Configure Tenant T0 Locale Services
6.  Configure Tenant T0 Interfaces
7.  Configure Tenant T0 Global BGP Neighbor
8.  Configure Tenant T0 BGP Neighbor (provider T0)
9.  Configure Tenant T1 Logical Router
10. Configure Production segment and attach to Tenant T1 Logical Router
11. Configure NAT for production segment.

Proceed with Caution, this is still in development.




