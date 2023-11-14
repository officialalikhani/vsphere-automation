from pyVmomi import vim
from tools import pchelper


def add_nic(si, vm, network_name):
    """
    :param si: Service Instance
    :param vm: Virtual Machine Object
    :param network_name: Name of the Virtual Network
    """
    spec = vim.vm.ConfigSpec()
    nic_changes = []

    nic_spec = vim.vm.device.VirtualDeviceSpec()
    nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

    nic_spec.device = vim.vm.device.VirtualE1000()

    nic_spec.device.deviceInfo = vim.Description()
    nic_spec.device.deviceInfo.summary = "vCenter API test"

    content = si.RetrieveContent()
    network = pchelper.get_obj(content, [vim.Network], network_name)
    if isinstance(network, vim.OpaqueNetwork):
        nic_spec.device.backing = (
            vim.vm.device.VirtualEthernetCard.OpaqueNetworkBackingInfo()
        )
        nic_spec.device.backing.opaqueNetworkType = network.summary.opaqueNetworkType
        nic_spec.device.backing.opaqueNetworkId = network.summary.opaqueNetworkId
    else:
        nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
        nic_spec.device.backing.useAutoDetect = False
        nic_spec.device.backing.deviceName = network_name

    nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    nic_spec.device.connectable.startConnected = True
    nic_spec.device.connectable.allowGuestControl = True
    nic_spec.device.connectable.connected = False
    nic_spec.device.connectable.status = "untried"
    nic_spec.device.wakeOnLanEnabled = True
    nic_spec.device.addressType = "assigned"

    nic_changes.append(nic_spec)
    spec.deviceChange = nic_changes
    vm.ReconfigVM_Task(spec=spec)
    print("NIC CARD ADDED")


def main(si, vm_name, port_group, uuid):
    """
    Sample for adding a NIC to vm
    """
    # parser = cli.Parser()
    # parser.add_required_arguments(cli.Argument.PORT_GROUP)
    # parser.add_optional_arguments(cli.Argument.VM_NAME, cli.Argument.UUID)
    # args = parser.get_args()
    # si = service_instance.connect(args)

    vm = None
    if uuid:
        search_index = si.content.searchIndex
        vm = search_index.FindByUuid(None, uuid, True)
    elif vm_name:
        content = si.RetrieveContent()
        vm = pchelper.get_obj(content, [vim.VirtualMachine], vm_name)

    if vm:
        add_nic(si, vm, port_group)
    else:
        print("VM not found")
