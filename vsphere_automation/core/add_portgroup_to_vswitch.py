import sys
import re
from pyVmomi import vim


def get_vm_hosts(content, regex_esxi=None):
    host_view = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.HostSystem], True
    )
    hosts = list(host_view.view)
    match_obj = []
    if regex_esxi:
        for esxi in hosts:
            if re.findall(r"%s.*" % regex_esxi, esxi.name):
                match_obj.append(esxi)
        match_obj_name = [match_esxi.name for match_esxi in match_obj]
        print("Matched ESXi hosts: %s" % match_obj_name)
        host_view.Destroy()
        return match_obj

    host_view.Destroy()
    return hosts


def add_hosts_portgroup(hosts, vswitch_name, portgroup_name, vlan_id):
    for host in hosts:
        add_host_portgroup(host, vswitch_name, portgroup_name, vlan_id)
    return True


def add_host_portgroup(host, vswitch_name, portgroup_name, vlan_id):
    portgroup_spec = vim.host.PortGroup.Specification()
    portgroup_spec.vswitchName = vswitch_name
    portgroup_spec.name = portgroup_name
    portgroup_spec.vlanId = int(vlan_id)
    network_policy = vim.host.NetworkPolicy()
    network_policy.security = vim.host.NetworkPolicy.SecurityPolicy()
    network_policy.security.allowPromiscuous = True
    network_policy.security.macChanges = False
    network_policy.security.forgedTransmits = False
    portgroup_spec.policy = network_policy

    host.configManager.networkSystem.AddPortGroup(portgroup_spec)


def main(si, esx_name_regex, vswitch_name, port_group, vlan_id):
    content = si.RetrieveContent()

    hosts = get_vm_hosts(content, esx_name_regex)
    if add_hosts_portgroup(hosts, vswitch_name, port_group, vlan_id):
        print("Added Port group to vSwitch")
