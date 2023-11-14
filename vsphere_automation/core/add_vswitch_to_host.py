from pyVmomi import vim


def get_vm_hosts(content):
    host_view = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.HostSystem], True
    )
    hosts = list(host_view.view)
    host_view.Destroy()
    return hosts


def add_hosts_switch(hosts, vswitch_name):
    for host in hosts:
        add_host_switch(host, vswitch_name)
    return True


def add_host_switch(host, vswitch_name):
    vswitch_spec = vim.host.VirtualSwitch.Specification()
    vswitch_spec.numPorts = 1024
    vswitch_spec.mtu = 1450
    host.configManager.networkSystem.AddVirtualSwitch(vswitch_name, vswitch_spec)


def main(si, vswitch_name):
    content = si.RetrieveContent()
    hosts = get_vm_hosts(content)
    if add_hosts_switch(hosts, vswitch_name):
        print("vSwitch Added")
