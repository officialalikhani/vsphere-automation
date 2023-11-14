from pyVmomi import vim


def get_vm_hosts(content):
    host_view = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.HostSystem], True
    )
    hosts = list(host_view.view)
    host_view.Destroy()
    return hosts


def del_hosts_portgroup(hosts, portgroup_name):
    for host in hosts:
        host.configManager.networkSystem.RemovePortGroup(portgroup_name)
    return True


def del_host_portgroup(host, portgroup_name):
    host.configManager.networkSystem.RemovePortGroup(portgroup_name)


def main(si, port_group):
    content = si.RetrieveContent()

    hosts = get_vm_hosts(content)
    if del_hosts_portgroup(hosts, port_group):
        print("Deleted Port Group")
