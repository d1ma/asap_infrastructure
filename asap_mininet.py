from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from argparse import ArgumentParser

import sys
import os
from util.monitor import monitor_qlen
from util.helper import stdev

lg.setLogLevel('info')

parser = ArgumentParser(description="ASAP Protocol Test")
parser.add_argument("--client_dns_bw", dest="client_dns_bw", type=float, default=62.5)
parser.add_argument("--client_dns_delay", dest="client_dns_delay", type=float, default=87)
parser.add_argument("--client_server_bw", dest="client_server_bw", type=float, default=62.5)
parser.add_argument("--client_server_delay", dest="client_server_delay", type=float, default=87)
parser.add_argument("--dns_server_bw", dest="dns_server_bw", type=float, default=62.5)
parser.add_argument("--dns_server_delay", dest="dns_server_delay", type=float, default=87)



class ASAPTopology(Topo):
    def build(self, client_dns_bw, client_dns_delay, dns_server_bw, dns_server_delay,
            client_server_bw, client_server_delay):
        # Setup switch
        client = self.addHost('client')
        dns = self.addHost('dns')
        server = self.addHost('server')

        self.addLink(client, dns, bw=client_dns_bw, delay=client_dns_delay)
        self.addLink(dns, server, bw=dns_server_bw, delay=dns_server_delay)
        self.addLink(client, server, bw=client_server_bw, delay=client_server_delay)



def main():
    start = time()


    topo = ASAPTopology(client_dns_bw, client_dns_delay, dns_server_bw, dns_server_delay,
            client_server_bw, client_server_delay)
    net - Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll()

    

if __name__=="__main__":
    if __name__ == '__main__':
    try:
        main()
    except:
        print "-"*80
        print "Caught exception.  Cleaning up..."
        print "-"*80
        import traceback
        traceback.print_exc()
        os.system("killall -9 top bwm-ng tcpdump cat mnexec iperf; mn -c")
