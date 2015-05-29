from mininet.topo import Topo
from mininet.node import CPULimitedHost, OVSController
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from argparse import ArgumentParser

import sys
import os

import subprocess
from subprocess import Popen, PIPE
from time import sleep, time
from argparse import ArgumentParser


lg.setLogLevel('info')

parser = ArgumentParser(description="ASAP Protocol Test")
parser.add_argument("--bw_host", dest="bw_host", type=float, default=62.5)
parser.add_argument("--bw_net", dest="bw_net", type=float, default=62.5)
parser.add_argument("--client_dns_delay", dest="delay", type=float, default=87)
parser.add_argument("--maxq", dest="maxq", default=1000)
parser.add_argument("--client_server_bw", dest="client_server_bw", type=float, default=62.5)
parser.add_argument("--client_server_delay", dest="client_server_delay", type=float, default=87)
parser.add_argument("--dns_server_bw", dest="dns_server_bw", type=float, default=62.5)
parser.add_argument("--dns_server_delay", dest="dns_server_delay", type=float, default=87)


class StarTopo(Topo):
    "Star topology for Buffer Sizing experiment"

    def build(self):
        # Setup switch
        switch = self.addSwitch('s0')

        # Setup receiver
        receiver = self.addHost('receiver')
        bw = 65.6
        delay = "87ms"
        maxq = 1000
        self.addLink(receiver, switch, bw=62.5, delay=delay, max_queue_size=maxq)

        # Setup senders
        num_senders = n - 1
        for i in range(num_senders):
            host = self.addHost('host%i' % i)
            self.addLink(host, switch, bw=1000)

        pass 

class ASAPTopology(Topo):
    def build(self):
        # Setup switch
        client = self.addHost('client')
        central_switch = self.addSwitch('client_switch')
        dns = self.addHost('dns')
        server = self.addHost('server')
        bw = 65.6
        delay = "87ms"
        self.addLink(client, central_switch, bw=bw, delay=delay, max_queue_size=1000)

        self.addLink(dns, central_switch, bw=bw, delay=delay, max_queue_size=1000)
        self.addLink(server, central_switch, bw=bw, delay=delay, max_queue_size=1000)
        pass


def main():
    args = parser.parse_args()
    start = time()

    topo = ASAPTopology()
    print "Starting mininet"
    print topo
    import pdb; pdb.set_trace()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=OVSController)
    net.start()
    print "Finished start"
    dumpNodeConnections(net.hosts)
    print "Hosts", net.hosts
    net.pingAll()

    net.stop()
    

if __name__=="__main__":
    try:
        main()
    except:
        print "-"*80
        print "Caught exception.  Cleaning up..."
        print "-"*80
        import traceback
        traceback.print_exc()
        os.system("killall -9 top bwm-ng tcpdump cat mnexec iperf; mn -c")
