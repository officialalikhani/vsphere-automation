import atexit, traceback
from pyVim.connect import SmartConnect, Disconnect
from .core.getallvms import main as main_GetVM
from .core.create_vm import create_vm as main_CreateVM
from .core.add_disk_to_vm import main as main_Add_Disk
from .core.add_nic_to_vm import main as main_add_nic
from .core.clone_vm import main as main_clone_vm
from .core.export_vm import main as main_export
from .core.snapshot_operations import main as main_snapshot
from .core.deploy_ova import main as main_deploy_ova
from .core.deploy_ovf import main as main_deploy_ovf
from .core.sessions_list import main as main_sessions
from .core.relocate_vm import main as main_relocate_vm
from .core.reboot_vm import reboot
from .core.vm_power_on import main as main_power_on
from .core.get_portgroup import main as main_get_portgroup
from .core.add_portgroup_to_vswitch import main as portgroup_to_vswitch
from .core.add_vswitch_to_host import main as vswitch_to_host
from .core.del_portgroup_from_vswitch import main as del_portgroup_from_vswitch
from .core.del_vswitch_from_host import main as del_vswitch_from_host

class VMwareAlikhani:
    def __init__(self, Hostadd_, Username_, Password_, Port_):
        self.host = Hostadd_
        self.user = Username_
        self.password = Password_
        self.port = Port_

    def __connect(self):
        """
        Determine the most preferred API version supported by the specified server,
        then connect to the specified server using that API version, login and return
        the service instance object.
        """
        service_instance = None
        try:
            service_instance = SmartConnect(
                host=self.host,
                user=self.user,
                pwd=self.password,
                port=self.port,
                disableSslCertValidation=True,
            )
            atexit.register(Disconnect, service_instance)
        except IOError as io_error:
            print(io_error)

        if not service_instance:
            raise SystemExit("Unable to connect to host with supplied credentials.")
        return service_instance

    def GetVMs(self):
        try:
            res = main_GetVM(self.__connect())
            return res
        except Exception:
            return traceback.format_exc()

    def CreateVM(self, vm_name, datacenter_name, host_ip):
        try:
            res = main_CreateVM(
                self.__connect(), vm_name, datacenter_name, host_ip, datastore_name=None
            )
            return res
        except Exception:
            return traceback.format_exc()

    def Add_Disk(self, vm_name, disk_size, disk_type, uuid=None):
        try:
            res = main_Add_Disk(
                self.__connect(), vm_name, disk_size, disk_type, uuid=None
            )
            return res
        except Exception:
            return traceback.format_exc()

    def Add_NIC(self, vm_name, port_group, uuid=None):
        try:
            res = main_add_nic(self.__connect(), vm_name, port_group, uuid=None)
            return res
        except Exception:
            return traceback.format_exc()

    def CloneVm(
        self,
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
        try:
            res = main_clone_vm(
                self.__connect(),
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
            )
            return res
        except Exception:
            return traceback.format_exc()

    def ExportVM(self, uuid, vm_name, workdir, name):
        try:
            res = main_export(self.__connect(), uuid, vm_name, workdir, name)
            return res
        except Exception:
            return traceback.format_exc()

    def Snapshot(self, vm_name, snapshot_operation, snapshot_name):
        try:
            res = main_snapshot(
                self.__connect(), vm_name, snapshot_operation, snapshot_name
            )
            return res
        except Exception:
            return traceback.format_exc()

    def Deploy_ova(self, datacenter_name, datastore_name, ova_path, host):
        try:
            res = main_deploy_ova(
                self.__connect(), datacenter_name, datastore_name, ova_path, host
            )
            return res
        except Exception:
            return traceback.format_exc()

    def Deploy_ovf(self, ovf_path, vmdk_path, host):
        try:
            res = main_deploy_ovf(self.__connect(), ovf_path, vmdk_path, host)
            return res
        except Exception:
            return traceback.format_exc()

    def Sessions(self):
        try:
            res = main_sessions(self.__connect())
            return res
        except Exception:
            return traceback.format_exc()

    def RelocateVM(self, datastore_name, esx_name, vm_name):
        try:
            res = main_relocate_vm(self.__connect(), datastore_name, esx_name, vm_name)
            return res
        except Exception:
            return traceback.format_exc()

    def Reboot(self, vm_name):
        try:
            res = reboot(self.__connect(), vm_name)
            return res
        except Exception:
            return traceback.format_exc()

    def PowerON(self, vm_name):
        try:
            res = main_power_on(self.__connect(), vm_name)
            return res
        except Exception:
            return traceback.format_exc()

    def GetPortgroup(self, port_group):
        try:
            res = main_get_portgroup(self.__connect(), port_group)
            return res
        except Exception:
            return traceback.format_exc()

    def Portgroup_to_vswitch(self, esx_name_regex, vswitch_name, port_group, vlan_id):
        try:
            res = portgroup_to_vswitch(
                self.__connect(), esx_name_regex, vswitch_name, port_group, vlan_id
            )
            return res
        except Exception:
            return traceback.format_exc()

    def Vswitch_to_Host(self, vswitch_name):
        try:
            res = vswitch_to_host(self.__connect(), vswitch_name)
            return res
        except Exception:
            return traceback.format_exc()

    def Del_portgroup_from_vswitch(self, port_group):
        try:
            res = del_portgroup_from_vswitch(self.__connect(), port_group)
            return res
        except Exception:
            return traceback.format_exc()
    
    def Del_vswitch_from_Host(self, vswitch_name):
        try:
            res = del_vswitch_from_host(self.__connect(), vswitch_name)
            return res
        except Exception:
            return traceback.format_exc()
