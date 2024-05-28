#!/usr/bin/python3

import argparse
import subprocess

def list_network_info():
    """Displays network interface information."""
    command = 'ip addr show'
    subprocess.run(command, shell=True)

def verify_connectivity(host):
    """Checks network connectivity by pinging the specified host."""
    command = f'ping -c 4 {host}'
    subprocess.run(command, shell=True)

def restart_networking():
    """Restarts the networking service and displays its status."""
    command = 'sudo systemctl restart networking && systemctl status networking'
    subprocess.run(command, shell=True)

def configure_interface(address, netmask, interface):
    """Configures the network interface with the provided IP address, netmask, and interface name."""
    command = f'sudo ip addr add {address}/{netmask} dev {interface} && '
    command += f'sudo ip link set {interface} up && '
    command += f'ip addr show {interface}'
    subprocess.run(command, shell=True)

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Perform various networking actions.")

    # Define command-line arguments
    parser.add_argument('action', choices=('list', 'verify', 'restart', 'configure'), help="Action to perform: 'list' to display network information, 'verify' to check connectivity, 'restart' to restart networking, 'configure' to configure network interface.")
    parser.add_argument('--host', help="Specify the host to ping (only used with 'verify' action).")
    parser.add_argument('--address', help="Specify the IP address for configuration (only used with 'configure' action).")
    parser.add_argument('--netmask', help="Specify the netmask for configuration (only used with 'configure' action).")
    parser.add_argument('--interface', help="Specify the network interface for configuration (only used with 'configure' action).")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Extract values from parsed arguments
    action = args.action
    host = args.host
    address = args.address
    netmask = args.netmask
    interface = args.interface

    # Perform the appropriate action based on user input
    match action:
        case 'list':
            list_network_info()
        case 'verify':
            verify_connectivity(host)
        case 'restart':
            restart_networking()
        case 'configure':
            configure_interface(address, netmask, interface)

if __name__ == "__main__":
    main()
