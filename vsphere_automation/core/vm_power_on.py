from pyVmomi import vim, vmodl
from samples.build.tools.tasks import wait_for_tasks


def main(si, vm_name):
    try:
        vmnames = vm_name
        if not vmnames:
            print("No virtual machine specified for poweron")

        # Retreive the list of Virtual Machines from the inventory objects
        # under the rootFolder
        content = si.content
        obj_view = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.VirtualMachine], True
        )
        vm_list = obj_view.view
        obj_view.Destroy()

        # Find the vm and power it on
        tasks = [vm.PowerOn() for vm in vm_list if vm.name in vmnames]

        # Wait for power on to complete
        wait_for_tasks(si, tasks)

        print("Virtual Machine(s) have been powered on successfully")
    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
    except Exception as error:
        print("Caught Exception : " + str(error))
