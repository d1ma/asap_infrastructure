from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
import time
from time import sleep

import timeit

import os

import matplotlib.pyplot as plt


dns=host=server=None

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        switch = self.addSwitch('s1')
        host = self.addHost('h')
        server = self.addHost('server')
        dns = self.addHost('dns')

        bw = 50
        delay = '23ms'
        loss = 1
        self.addLink(host, switch,bw=bw, delay=delay, loss=loss, use_htb=True)
        self.addLink(server, switch,bw=bw, delay=delay, loss=loss, use_htb=True)
        self.addLink(dns, switch,bw=bw, delay=delay, loss=loss, use_htb=True)

def getLatency(sender, receiver):
    latency = float(sender.cmd("ping -c 1 %s | tail -1 | awk -F '/' '{print $5}'" % receiver.IP()))
    return latency


def printLatencyStats():
    print ("#### [ Latency stats ] ####")
    print "host <-> server", getLatency(host, server)
    print "dns <-> server", getLatency(dns, server)
    print "dns <-> host", getLatency(dns, host)

def write_plot_cdf(output, savepath):
    x = sorted(output)
    y = [float(i) / len(x) for i in enumerate(x)]

    plt.plot(x,y)
    plt.savefig(savepath)

def write_results(output):

    if not os.path.exists('results'):
        os.makedirs('results')

    result_name = "run_%i" % int(time.time())
    with open(os.path.join("results", result_name), 'w') as out_f:
        out_f.write("\n".join(output))
    return result_name


    
def perfTest():
    "Create network and run simple performance test"
    topo = SingleSwitchTopo( )
    net = Mininet( topo=topo,
                   host=CPULimitedHost, link=TCLink,
                   autoStaticArp=True, controller=OVSController )
    net.start()
    # print "Dumping host connections"
    # dumpNodeConnections(net.hosts)
    global host, server, dns

    host, server, dns = net.getNodeByName('h', 'server', 'dns')
    # net.iperf( ( h1, h4 ), l4Type='UDP' )
    print "Starting python server"
    server.cmd("python -m SimpleHTTPServer 80 &")
    sleep(0.5) # enough for the server to start-up

    output = []
    for t in range(30):            
        print "Starting to time wget"
        result = host.cmd('perf stat wget --quiet %s' % server.IP())
        print result

    result_name = write_results(output)
    write_results(output, result_name + ".png")
    # end_seconds = result.index("seconds time elapsed")
    # start_seconds = result[:end_seconds].rindex("   ")
    # print "Extracted time:", float(result[start_seconds:end_seconds])
    import re
    line_match = re.search("[\d. ]+seconds time elapsed", result).group()
    secs = float(re.search("\d+.\d+", line_match).group())

    print "Extracted time", secs


    # print result


    # print host.cmd('wget --quiet %s' % server.IP())




    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    perfTest()