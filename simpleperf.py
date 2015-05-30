from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.cli import CLI

import time
from time import sleep
import timeit
import os
import re

import matplotlib.pyplot as plt

from argparse import ArgumentParser


bw = 3
delay = '23ms'
loss = 0




class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        switch = self.addSwitch('s1')
        host = self.addHost('h')
        server = self.addHost('server')
        dns = self.addHost('dns')

        self.addLink(host, switch, bw=bw, delay='80ms', loss=loss, use_htb=True)
        self.addLink(server, switch, bw=bw, delay='0ms', loss=loss, use_htb=True)
        self.addLink(dns, switch, bw=bw, delay='0ms', loss=loss, use_htb=True)

def getLatency(sender, receiver):
    latency = float(sender.cmd("ping -c 1 %s | tail -1 | awk -F '/' '{print $5}'" % receiver.IP()))
    return latency


def printLatencyStats(net):
    host, server, dns = net.getNodeByName('h', 'server', 'dns')
    print ("#### [ Latency stats ] ####")
    print "host <-> server", getLatency(host, server)
    print "dns <-> server", getLatency(dns, server)
    print "dns <-> host", getLatency(dns, host)

def write_results(output, file_prefix):
    if not os.path.exists('results'):
        os.makedirs('results')

    result_name = "%s_%i.txt" % (file_prefix, int(time.time()))
    result_path = os.path.join("results", result_name)
    with open(os.path.join("results", result_name), 'w') as out_f:
        out_f.write("\n".join([str(o) for o in output]))
    return result_path

def rttTest(net):
    "Create network and run simple performance test"
    host, server, dns = net.getNodeByName('h', 'server', 'dns')
    print "Starting python server"
    server.cmd("python -m SimpleHTTPServer 80 &")
    sleep(0.5) # enough for the server to start-up

    output = []
    for t in range(20):            
        result = get_latency(host, server)
        output += [secs]
        print secs

    result_name = write_results(output, "rtt")
    print "Done, results written to %s" % result_name


def perfTest(net):
    "Create network and run simple performance test"
    host, server, dns = net.getNodeByName('h', 'server', 'dns')
    print "Starting python server"
    server.cmd("python -m SimpleHTTPServer 80 &")
    sleep(0.5) # enough for the server to start-up

    output = []
    for t in range(20):            
        result = host.cmd('perf stat curl -s %s 1>/dev/null' % server.IP())
        line_match = re.search("[\d. ]+seconds time elapsed", result).group()
        secs = float(re.search("\d+.\d+", line_match).group())
        output += [secs]
        print secs

    result_name = write_results(output, "perf")
    print "Done, results written to %s" % result_name

def udtTest(net):
    host, server, dns = net.getNodeByName('h', 'server', 'dns')
    print "Starting server"
    server.cmd("~/asap/appserver --asap=0 &")
    dns.cmd("cd ~/asap/userspace/adns; sudo ./build_dns.bash %s" % server.IP())

    output = []
    print "go"
    for t in range(20):            
        result = host.cmd('perf stat ~/asap/appclient --dns-ip=%s --asap=0' % dns.IP())
        line_match = re.search("[\d. ]+seconds time elapsed", result).group()
        secs = float(re.search("\d+.\d+", line_match).group())
        output += [secs]
        print secs

    result_name = write_results(output, "udt")
    print "Done, results written to %s" % result_name

def asapTest(net):
    host, server, dns = net.getNodeByName('h', 'server', 'dns')
    print "Starting server"
    server.cmd("~/asap/appserver --asap=1 &")
    dns.cmd("cd ~/asap/userspace/adns; sudo ./build_dns.bash %s" % server.IP())

    output = []
    print "go"
    for t in range(20):            
        result = host.cmd('perf stat ~/asap/appclient --dns-ip=%s --asap=1' % dns.IP())
        line_match = re.search("[\d. ]+seconds time elapsed", result).group()
        secs = float(re.search("\d+.\d+", line_match).group())
        output += [secs]
        print secs

    result_name = write_results(output, "asap")
    print "Done, results written to %s" % result_name

def main():
    topo = SingleSwitchTopo()
    net = Mininet(topo=topo,
                  host=CPULimitedHost, link=TCLink,
                  autoStaticArp=True, controller=OVSController)
    net.start()
    # print "Dumping host connections"
    # dumpNodeConnections(net.hosts)
    #CLI(net)
    perfTest(net)
    udtTest(net)
    asapTest(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')   
    main()
