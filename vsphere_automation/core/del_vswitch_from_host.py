from pyVmomi import vim

def get_vm_hosts(content):
    host_view = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.HostSystem], True
    )
    hosts = list(host_view.view)
    host_view.Destroy()
    return hosts


def del_hosts_switch(hosts, vswitch_name):
    for host in hosts:
        del_host_switch(host, vswitch_name)
    return True


def del_host_switch(host, vswitch_name):
    host.configManager.networkSystem.RemoveVirtualSwitch(vswitch_name)


def main(si,vswitch_name):
    content = si.RetrieveContent()

    hosts = get_vm_hosts(content)
    if del_hosts_switch(hosts, vswitch_name):
        print("vSwitch Deleted")


