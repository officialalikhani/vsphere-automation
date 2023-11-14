from tools import pchelper
from pyVmomi import vmodl, vim


def main(si, port_group):
    try:
        content = si.RetrieveContent()

        # searching for port group
        port_group = pchelper.get_obj(content, [vim.Network], port_group)
        print(port_group)

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : {0}".format(error.msg))
        return -1

    return 0
