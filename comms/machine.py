
import serial.tools.list_ports as port_list


def ListAllPorts():
    '''List all available ports on the machine.'''
    allports = list(port_list.comports())
    print("Listing all available ports on machine:\n")
    for port in allports:
        print(port)
    print('\n')


class Machine:

    PortsInUse = []
    AvailablePorts = []
    status = False

    def init():
        allports = list(port_list.comports())
        Machine.AvailablePorts = [p.name for p in allports]

        # Print Ports on the screen
        ListAllPorts()
        Machine.status = (True)

    def RegisterPort(port):

        if not Machine.status:
            Machine.init()

        if port in Machine.PortsInUse:
            print(f"ERROR port : {port} is already being used by another device.")
            return False
        elif port not in Machine.AvailablePorts:
            print(f"ERROR {port} : no such port exists.")
            return False
        else:
            return True

    def DeRegisterPort(port):
        if port in Machine.PortsInUse:
            Machine.PortsInUse.pop(Machine.AvailablePorts.index(port))
