import socket
import ipaddress
import netaddr
import netifaces
import json
from datetime import datetime

def netwrokadapterdata():
    for i in range(0,(len(netifaces.interfaces()))):
        q = netifaces.ifaddresses(netifaces.interfaces()[i])
        p =list((q.values()))
        for j in range(0,len(p)):
            t = p[j]
            for k in range(0,len(t)):
                a = t[k]
                for value in a.values():
                    if value ==socket.gethostbyname(socket.gethostname()):
                        prefix = netaddr.IPAddress(a['netmask']).netmask_bits()
                        host = ipaddress.ip_interface(
                            str(socket.gethostbyname(socket.gethostname())) + '/' + str(prefix))
                        networkid= str(host.network)
                        networkid=networkid.split('/')[0]
                        return (prefix,a['netmask'], a['broadcast'],networkid)

def networkmap(prefix,networkid):
    net_addr =str(networkid) +'/'+str(prefix)
    ip_net = ipaddress.ip_network(net_addr)
    networkmaper = str(list(ip_net.hosts()))
    temp = networkmaper.replace('IPv4Address(','')
    ids = temp.replace('),','')
    ids = ids.replace("'", "")
    return (ids)


def scan(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(0.5)
    result = s.connect_ex((addr,135))
    if result == 0:
        return 1
    else:
        return 0

def run1(networkmap):
    networkmap= networkmap.replace("[", "")
    networkmap = networkmap.replace(")]", "")
    for ip in networkmap.split():
        print(ip)
        if (scan(ip)):
           print(ip, socket.gethostbyaddr(ip)[0], "is live")
           logger(ip)


def logger(ip):
    data2save = [ip,socket.gethostbyaddr(ip)[0]]+['is live']
    with open('live_devices.json', 'a+') as f:
        json.dump(data2save, f)
        f.write('\n')
    return()

t1 = datetime.now()

a = networkmap(netwrokadapterdata()[0],netwrokadapterdata()[3])
run1(a)
t2 = datetime.now()
total = t2 - t1
print("Scanning completed in: ", total)



