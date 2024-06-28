#!/usr/bin/python3

import argparse
import subprocess

def list_network_info():
    """Displays network interface information."""
    command = ['ip', 'addr', 'show']
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error executing command: {e}')

def verify_connectivity(host):
    """Checks network connectivity by pinging the specified host."""
    command = ['ping', '-c', '4', host]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error executing command: {e}')

def restart_networking():
    """Restarts the networking service and displays its status."""
    restart_command = ['sudo', 'systemctl', 'restart', 'networking']
    status_command = ['systemctl', 'status', 'networking']
    try:
        subprocess.run(restart_command, check=True)
        subprocess.run(status_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error executing command: {e}')

def configure_interface(address, netmask, interface):
    """Configures the network interface with the provided IP address, netmask, and interface name."""
    configure_command = ['sudo', 'ip', 'addr', 'add', f'{address}/{netmask}', 'dev', interface]
    up_command = ['sudo', 'ip', 'link', 'set', interface, 'up']
    show_command = ['ip', 'addr', 'show', interface]
    try:
        subprocess.run(configure_command, check=True)
        subprocess.run(up_command, check=True)
        subprocess.run(show_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error executing command: {e}')

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
    if action == 'list':
        list_network_info()
    elif action == 'verify':
        if host:
            verify_connectivity(host)
        else:
            print('Host is required for verify action.')
    elif action == 'restart':
        restart_networking()
    elif action == 'configure':
        if address and netmask and interface:
            configure_interface(address, netmask, interface)
        else:
            print('Address, netmask, and interface are required for configure action.')

if __name__ == "__main__":
    main()
