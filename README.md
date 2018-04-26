# IPv4 Subnet Calculation in Python3
List a network definition for a given IPv4 address entered by the user which includes
- Network Address
- Broadcast Address
- Subnet mask
- Host/wildcard mask
- User's requested number of valid hosts

Prior to listing, data validation is carried out based on the following criteria
- A valid IPv4 address which also exludes the following valid IPv4 addresse space
  - 127.0.0.0/8 (loopback addresses)
  - 169.254.0.0/16 (APIPA Addresses)
  - 0.0.0.0/8 (Software Scope Addresses)
- A valid subnet mask

## Getting Started
`python3 subnet.py`
## Prerequisites
Need python3 as the script uses the ipaddress module
## Example
```
Enter a unicast IPv4 address excluding 127.0.0.0/24, 0.0.0.0/8, 169.254.0.0/26: 192.168.2.200
Enter subnet mask: 255.255.255.128

----Network Definition for 192.168.2.200 255.255.255.128----

    Network Address:   192.168.2.128  
    Broadcast Address: 192.168.2.255  
    Valid Hosts:       126            
    Wildcard Mask:     0.0.0.127      
    Mask bits:         25             
Do you want to generate valid IP host addresses: [Y/N]y
Enter number of hosts Max 126: 7
Valid Host IPv4 addresses for this subnet:['192.168.2.129', '192.168.2.130', '192.168.2.131', '192.168.2.132', '192.168.2.133', '192.168.2.134', '192.168.2.135']
```
