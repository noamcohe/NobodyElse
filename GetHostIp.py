"""
Get the IP address of the host
"""


import os
import sys


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
