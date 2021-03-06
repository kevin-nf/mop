#!/usr/bin/python3
"""Create VWAN."""
import os
from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import ServicePrincipalCredentials

# setup Azure Login Credentials from Environmental Variables
credentials = ServicePrincipalCredentials(
    client_id=os.environ.get('ARM_CLIENT_ID'),
    secret=os.environ.get('ARM_CLIENT_SECRET'),
    tenant=os.environ.get('ARM_TENANT_ID')
)

# declaire Test Input Variables
VWAN_PARAMS = {
    'location': os.environ.get('LOCATION'),
    'tags': {
        'key1': os.environ.get('KEY1')
    },
    'disable_vpn_encryption': False,
    'allow_branch_to_branch_traffic': True,
    'allow_vnet_to_vnet_traffic': True,
    'office365_local_breakout_category': 'None',
    'type': 'Basic'
}
VHUB_PARAMS = {
    'location': os.environ.get('LOCATION'),
    'tags': {
        'key1': os.environ.get('KEY1')
    },
    'virtual_network_connections': [],
    'address_prefix': os.environ.get('VHUB_PREFIX'),
    'route_table': {
      "routes": []
    },
    'virtual_wan': {
      'id': "/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/virtualWans/%s" % (os.environ.get('ARM_SUBSCRIPTION_ID'), os.environ.get('GROUP_NAME'), os.environ.get('VWAN_NAME'))
    },
    'sku': 'Basic'
}
VPNG_PARAMS = {
    'location': os.environ.get('LOCATION'),
    'tags': {
        'key1': os.environ.get('KEY1')
    },
    'bgp_settings': {
      'asn': 65515,
      'peer_weight': 0
    },
    'virtual_hub': {
      'id': "/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/virtualHubs/%s" % (os.environ.get('ARM_SUBSCRIPTION_ID'), os.environ.get('GROUP_NAME'), os.environ.get('VHUB_NAME'))
    },
    'vpn_gateway_scale_unit': 1
}

# Connect to Azure APIs and get session details
network_client = NetworkManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))

# Create VWAN
async_vwan_creation = network_client.virtual_wans.create_or_update(
    os.environ.get('GROUP_NAME'),
    os.environ.get('VWAN_NAME'),
    VWAN_PARAMS,
    custom_headers=None,
    raw=False,
    polling=True
)
async_vwan_creation.wait()
print(async_vwan_creation.result())

# Create VHUB
async_vhub_creation = network_client.virtual_hubs.create_or_update(
    os.environ.get('GROUP_NAME'),
    os.environ.get('VHUB_NAME'),
    VHUB_PARAMS,
    custom_headers=None,
    raw=False,
    polling=True
)
async_vhub_creation.wait()
print(async_vhub_creation.result())
