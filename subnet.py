#!/usr/bin/env python3.6
# Author: M Khoudi
''' Purpose: validate entry of IPv4 unicast address excluding:
             loopback addresses{127.0.0.0/8},
             APIPA addresses[169.254.0.0/16]
             Software scope addresses: 0.0.0.0/8
             Also, validate entry of Ipv4 mask address
             Prints out the network definition which include:
             Network address, Broadcast address, valid hosts,
             host/wildcard address, prefixlen
             Provide a requested number of valid host addresses for the user'''


import sys
import ipaddress


def define_network(*addr):
    """gives all network related data or host addresses if requested

    addr = tuple of arguments netaddr/mask[nb of requested hosts]
    """

    if len(addr) == 2:
        # provides list of host-addresses for this subnet
        # we do this by calling the generator host_g
        host_g = addr[0].hosts()
        return [next(host_g).exploded for i in range(addr[1])]
    else:
        netdef = [('    Network Address:',
                   addr[0].network_address.exploded),
                  ('    Broadcast Address:',
                   addr[0].broadcast_address.exploded),
                  ('    Valid Hosts:', 2 ** (32 - addr[0].prefixlen)-2),
                  ('    Wildcard Mask:', addr[0].hostmask.exploded),
                  ('    Mask bits:', addr[0].prefixlen),
                  ]
        return [('    '+addr[0].network_address.exploded+'/32', '')] \
            if addr[0].prefixlen == 32 else netdef


def print_net_def(net_data, req_host_addr):
    """print all IPv4 data related to this network

    :param net_data: list of network data or
                     list of requested hosts addresses for this subnet
    """
    if req_host_addr:
        # Print list of requested host addresses
        title = "Valid Host IPv4 addresses for this subnet:"
        print(f"{title:<41}", end='')
        print(net_data)
    else:
        title = 'Network Definition for ' + ip.exploded + ' ' + subnet_mask
        print("\n{:-^60}\n".format(title))
        for data, value in net_data:
            print(f"{data:<23}{value:<15}")


def is_ip_valid():
    """is_ip_valid:  check if a given ip address is valid
       a valid ip address is a unicast Class A , B ,C but excluding
       Loopback addresses: 127.0.0.0/8
       Software scope addresses: 0.0.0.0/8
       APIPA addresses(lack of ip address): 169.254.0.0/16


    :param ip: ip address
    """
    exec_addr = "127.0.0.0/24, 0.0.0.0/8, 169.254.0.0/26: "
    global ip
    ip = input("Enter a unicast IPv4 address excluding " + exec_addr)
    try:
        ip = ipaddress.ip_address(ip)
    except ValueError:
        # print("{} is neither an IPv4 nor IPv6 address".format(ip))
        return False
    # test if ip address conform to the requirement as def in docstring
    if any([ip.is_link_local, ip.is_loopback, ip.is_multicast, ip.is_reserved,
            ip.compressed[0] == '0']):
        return False
    else:
        return True


def is_mask_valid():
    """is_valid_mask: Check if the mask is valid
    Validity test: mask [255, 254, 252, 248, 240, 224, 192, 128, 0]
    first octet must be 255|0 subsequent octets must be in descending order

    :param mask: IPv4 address of type string
    """
    global subnet_mask
    subnet_mask = input("Enter subnet mask: ")
    # mov is the possible mask octet values
    mov = [255 << i & 255 for i in range(9)]
    # check if mask contains only valid octet
    mask = [int(x) for x in subnet_mask.split('.') if int(x) in mov]
    # check mask conforms with 4 octets in descending order
    if len(mask) == 4 and mask[0] == 255 and \
       all(prev >= next for prev, next in zip(mask, mask[1:])):
        return True
    else:
        return False


def main():
    try:
        while not is_ip_valid():
            print(" Not a valid IP address Try again!")
        while not is_mask_valid():
            print(" Not a valid subnet mask, Try again!")

        # ip and mask are valid. get list of network octets(lno) by & operation
        lno = [str(int(x) & int(y)) for x, y in zip(ip.exploded.split('.'),
                                                    subnet_mask.split('.'))]
        # netaddr: network addr followed by sbnet mask
        netaddr = ipaddress.IPv4Network('.'.join(lno)+'/'+subnet_mask)
        # get the network definition for this network address
        net_def = define_network(netaddr)
        print_net_def(net_def, req_host_addr=False)
        # ask user if they want to generate ip host addresses
        if netaddr.prefixlen == 32:
            print("This is a 32 bit network host")
        else:
            while True:
                answer = input("Do you want to generate "
                               "valid IP host addresses: [Y/N]")
                if answer.upper() not in ('Y', 'N'):
                    print("Answer must be [Y/N]")
                    continue
                if answer.upper() == 'Y':
                    message = "Enter number of hosts Max " \
                              + str(net_def[2][1]) + ": "
                    try:
                        nb_of_addrs = int(input(message))
                        if not (0 < nb_of_addrs < net_def[2][1]):
                            print("Number of hosts must be > 1 "
                                  "and cannot exceed {:3d}"
                                  " in this subnet".format(net_def[2][1]))
                            break
                        lhost_addrs = define_network(netaddr, nb_of_addrs)
                        print_net_def(lhost_addrs, req_host_addr=True)
                        break
                    except ValueError:
                        print("you have entered a non integer value:")
                        continue
                break
    except KeyboardInterrupt:
        print("Program aborted by the user. Exiting...")
        sys.exit()


if __name__ == "__main__":
    main()
