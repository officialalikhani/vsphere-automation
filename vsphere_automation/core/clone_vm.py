"""
Clone a VM from template example
"""
from pyVmomi import vim
from ..tools import pchelper
from .add_nic_to_vm import add_nic


def wait_for_task(task):
    """wait for a vCenter task to finish"""
    task_done = False
    while not task_done:
        if task.info.state == "success":
            return task.info.result

        if task.info.state == "error":
            print("there was an error")
            print(task.info.error)
            task_done = True


def clone_vm(
    content,
    template,
    vm_name,
    datacenter_name,
    vm_folder,
    datastore_name,
    cluster_name,
    resource_pool,
    power_on,
    datastorecluster_name,
):
    """
    Clone a VM from a template/VM, datacenter_name, vm_folder, datastore_name
    cluster_name, resource_pool, and power_on are all optional.
    """

    # if none git the first one
    datacenter = pchelper.get_obj(content, [vim.Datacenter], datacenter_name)

    if vm_folder:
        destfolder = pchelper.search_for_obj(content, [vim.Folder], vm_folder)
    else:
        destfolder = datacenter.vmFolder

    if datastore_name:
        datastore = pchelper.search_for_obj(content, [vim.Datastore], datastore_name)
    else:
        datastore = pchelper.get_obj(
            content, [vim.Datastore], template.datastore[0].info.name
        )

    # if None, get the first one
    cluster = pchelper.search_for_obj(
        content, [vim.ClusterComputeResource], cluster_name
    )
    if not cluster:
        clusters = pchelper.get_all_obj(content, [vim.ResourcePool])
        cluster = list(clusters)[0]

    if resource_pool:
        resource_pool = pchelper.search_for_obj(
            content, [vim.ResourcePool], resource_pool
        )
    else:
        resource_pool = cluster.resourcePool
    vmconf = vim.vm.ConfigSpec()

    if datastorecluster_name:
        podsel = vim.storageDrs.PodSelectionSpec()
        pod = pchelper.get_obj(content, [vim.StoragePod], datastorecluster_name)
        podsel.storagePod = pod
        storagespec = vim.storageDrs.StoragePlacementSpec()
        storagespec.podSelectionSpec = podsel
        storagespec.type = "create"
        storagespec.folder = destfolder
        storagespec.resourcePool = resource_pool
        storagespec.configSpec = vmconf
        try:
            rec = content.storageResourceManager.RecommendDatastores(
                storageSpec=storagespec
            )
            rec_action = rec.recommendations[0].action[0]
            real_datastore_name = rec_action.destination.name
        except Exception:
            real_datastore_name = template.datastore[0].info.name
        datastore = pchelper.get_obj(content, [vim.Datastore], real_datastore_name)
    relospec = vim.vm.RelocateSpec()
    relospec.datastore = datastore
    relospec.pool = resource_pool
    clonespec = vim.vm.CloneSpec()
    clonespec.location = relospec
    clonespec.powerOn = power_on
    print("cloning VM...")
    task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
    wait_for_task(task)
    print("VM cloned.")


def main(
    si,
    template,
    vm_name,
    datacenter_name,
    vm_folder,
    datastore_name,
    cluster_name,
    resource_pool,
    power_on,
    datastorecluster_name,
    opaque_network_name,
):
    content = si.RetrieveContent()
    template = pchelper.get_obj(content, [vim.VirtualMachine], template)

    if template:
        clone_vm(
            content,
            template,
            vm_name,
            datacenter_name,
            vm_folder,
            datastore_name,
            cluster_name,
            resource_pool,
            power_on,
            datastorecluster_name,
        )
        if opaque_network_name:
            vm = pchelper.get_obj(content, [vim.VirtualMachine], vm_name)
            add_nic(si, vm, opaque_network_name)
    else:
        print("template not found")
