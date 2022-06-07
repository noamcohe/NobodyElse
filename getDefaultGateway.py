"""
Get the default gateway IP address
"""


# Some imports:
import os
import sys


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
