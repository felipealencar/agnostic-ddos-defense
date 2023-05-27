from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, Controller, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI

def create_iot_network():
    # Create a Mininet instance
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch, link=TCLink)

    # Add a remote controller
    controller = net.addController('c0', ip='127.0.0.1', port=6653)

    # Add switches and IoT devices
    switch = net.addSwitch('s1')

    # Add IoT gateway
    gateway = net.addHost('gateway')

    # Add IoT devices
    devices = []
    for i in range(1, 6):
        device = net.addHost(f'device{i}')
        devices.append(device)

    # Create links between the devices and the switch
    for device in devices:
        net.addLink(device, switch)

    # Create a link between the gateway and the switch
    net.addLink(gateway, switch)

    # Build the network
    net.build()

    # Start the controller and switches
    controller.start()
    switch.start([controller])

    # Set IP addresses for the devices
    gateway.cmd('ifconfig gateway-eth0 192.168.0.1/24')
    for i, device in enumerate(devices, start=1):
        device.cmd(f'ifconfig device{i}-eth0 192.168.0.{i + 1}/24')

    # Enable IP forwarding on the gateway
    gateway.cmd('sysctl net.ipv4.ip_forward=1')

    # Set default routes on the devices
    for device in devices:
        device.cmd(f'route add default gw 192.168.0.1')

    # Open the Mininet command line interface
    CLI(net)

    # Clean up the network
    net.stop()


if __name__ == '__main__':
    create_iot_network()
