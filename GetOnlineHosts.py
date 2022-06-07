"""
Get a list of hosts that are online.
"""


import nmap


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
