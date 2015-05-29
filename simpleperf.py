from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController


class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        switch = self.addSwitch('s1')
        host = self.addHost('h')
        server = self.addHost('server')
        dns = self.addHost('dns')

        self.addLink(host, switch,bw=10, delay='5ms', loss=0, use_htb=True)
        self.addLink(server, switch,bw=10, delay='5ms', loss=0, use_htb=True)
        self.addLink(dns, switch,bw=10, delay='5ms', loss=0, use_htb=True)

def getLatency(sender, receiver):
    latency = float(sender.cmd("ping -c 1 %s | tail -1 | awk -F '/' '{print $5}'" % receiver.IP()))
    return latency


def printLatencyStats():
    print ("#### [ Latency stats ] ####")
    print "host <-> server", getLatency(host, server)
    print "dns <-> server", getLatency(dns, server)
    print "dns <-> host", getLatency(dns, host)

    
def perfTest():
    "Create network and run simple performance test"
    topo = SingleSwitchTopo( )
    net = Mininet( topo=topo,
                   host=CPULimitedHost, link=TCLink,
                   autoStaticArp=True, controller=OVSController )
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing bandwidth between host and server"

    host, server, dns = net.getNodeByName('h', 'server', 'dns')
    # net.iperf( ( h1, h4 ), l4Type='UDP' )




    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    perfTest()