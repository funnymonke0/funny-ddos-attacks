import socks
import socket
import time
import argparse



def load_proxies(name):
        port = []
        addr = []
        with open(name, 'r') as file:
              for i in file.readlines():
                    i = i.replace('socks5://', '')
                    i = i.replace(' ', '')
                    addrport = i.split(':')
                    addr.append(addrport[0])
                    port.append(int(addrport[1]))
        return addr, port

def tryproxy(addr, port):
        working = []
        socket.socket = socks.socksocket
        for i in range(0, len(addr)):
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, addr[i], port[i])
                
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                print(str(round((i/len(addr))*100, 2))+" %" +" done...", end='\r')
                try:
                        s.connect(('www.google.com', 80))

                except socks.ProxyConnectionError:
                        continue
                except socks.GeneralProxyError:
                        continue
                else:
                        working.append((addr[i], port[i]))
                        print(f'candidate found: {addr[i]}: {port[i]}')
                        continue
        return working

def main():
        

        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--file-name',
                            default='socks5.txt',
                            dest='filename',
                            type = str)
        parser.add_argument('-s', '--save',
                            dest='save',
                            action= "store_true")
        parser.add_argument('-n', '--save-name',
                            default= 'results',
                            dest='savename',
                            type = str)
        args = parser.parse_args()
        filename = args.filename
        proctime = time.process_time()
        addrs, ports = load_proxies(filename)
        working = tryproxy(addrs, ports)
        
        print(f'Done in {proctime} sec')
        print(working)
        savename = (args.savename).replace('.txt', '')
        savename = savename + '.txt'
        if args.save:
                with open(savename, 'w') as file:
                        for entry in working:
                                ip = str(entry[0])
                                port = str(entry[1])
                                file.write(f'{ip}:{port}\n')
                print(f'{working} saved in {savename}')
main()