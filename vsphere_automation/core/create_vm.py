import sys
from pyVmomi import vim
from pyVim.task import WaitForTask
from tools import pchelper


def create_vm(si, vm_name, datacenter_name, host_ip, datastore_name=None):
    content = si.RetrieveContent()
    destination_host = pchelper.get_obj(content, [vim.HostSystem], host_ip)
    source_pool = destination_host.parent.resourcePool
    if datastore_name is None:
        datastore_name = destination_host.datastore[0].name

    config = create_config_spec(datastore_name=datastore_name, name=vm_name)
    for child in content.rootFolder.childEntity:
        if child.name == datacenter_name:
            vm_folder = child.vmFolder  # child is a datacenter
            break
    else:
        print("Datacenter %s not found!" % datacenter_name)
        sys.exit(1)

    try:
        WaitForTask(vm_folder.CreateVm(config, pool=source_pool, host=destination_host))
        print("VM created: %s" % vm_name)
    except vim.fault.DuplicateName:
        print("VM duplicate name: %s" % vm_name, file=sys.stderr)
    except vim.fault.AlreadyExists:
        print("VM name %s already exists." % vm_name, file=sys.stderr)


def create_config_spec(
    datastore_name, name, memory=4, guest="otherGuest", annotation="Sample", cpus=1
):
    config = vim.vm.ConfigSpec()
    config.annotation = annotation
    config.memoryMB = int(memory)
    config.guestId = guest
    config.name = name
    config.numCPUs = cpus
    files = vim.vm.FileInfo()
    files.vmPathName = "[" + datastore_name + "]"
    config.files = files
    return config
