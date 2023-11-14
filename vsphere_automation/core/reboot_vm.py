from tools import pchelper, tasks
from pyVmomi import vim


def reboot(si, vm_name):
    content = si.RetrieveContent()
    VM = pchelper.get_obj(content, [vim.VirtualMachine], vm_name)

    if VM is None:
        raise SystemExit("Unable to locate VirtualMachine.")

    print("Found: {0}".format(VM.name))
    print("The current powerState is: {0}".format(VM.runtime.powerState))
    TASK = VM.ResetVM_Task()
    tasks.wait_for_tasks(si, [TASK])
    print("its done.")
