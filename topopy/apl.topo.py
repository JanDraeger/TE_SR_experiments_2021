
#!/usr/bin/env python3
from node import *

class apl(Topo):
    def build(self):
        self.add_node("0")
        self.add_node("1")
        self.add_node("2")
        self.add_node("3")
        self.add_node("4")
        self.add_node("5")
        self.add_link_name("0", "1", cost=1000, delay=0.2, bw=2000000000000.0, directed=True)
        self.add_link_name("1", "0", cost=1000, delay=0.2, bw=2000000000000.0, directed=True)
        self.add_link_name("1", "2", cost=1000, delay=0.2, bw=2000000000000.0, directed=True)
        self.add_link_name("2", "1", cost=1000, delay=0.2, bw=2000000000000.0, directed=True)
        self.add_link_name("1", "3", cost=1000, delay=0.2, bw=2000000000000.0, directed=True)
        self.add_link_name("3", "1", cost=1000, delay=0.2, bw=2000000000000.0, directed=True)
        self.add_link_name("1", "4", cost=1000, delay=0.2, bw=1000000000000.0, directed=True)
        self.add_link_name("4", "1", cost=1000, delay=0.2, bw=1000000000000.0, directed=True)
        self.add_link_name("2", "4", cost=1000, delay=0.2, bw=2000000000000.0, directed=True)
        self.add_link_name("4", "2", cost=1000, delay=0.2, bw=2000000000000.0, directed=True)
        self.add_link_name("3", "4", cost=1000, delay=0.2, bw=2000000000000.0, directed=True)
        self.add_link_name("4", "3", cost=1000, delay=0.2, bw=2000000000000.0, directed=True)
        self.add_link_name("4", "5", cost=1000, delay=0.2, bw=2000000000000.0, directed=True)
        self.add_link_name("5", "4", cost=1000, delay=0.2, bw=2000000000000.0, directed=True)
    
    def dijkstra_computed(self):
        # Demand from 0 to 5
        build_str = ""
        nhlist = self.get_dijkstra_route_by_name("0","2")
        for nh in nhlist:
            build_str += f" nexthop via {nh.nh} "+" encap seg6 mode inline segs {2} "+ f" weight {int(100/len(nhlist))} "
        self.add_command("0", f"ip -6 route add {{5}} metric 1 table 1 src {{0}}  {build_str}")
        # Demand from 2 to 3
        build_str = ""
        self.add_command("2", f"ip -6 route add {{3}} metric 1 table 1 src {{2}}  {build_str}")
        # Demand from 0 to 4
        build_str = ""
        nhlist = self.get_dijkstra_route_by_name("0","2")
        for nh in nhlist:
            build_str += f" nexthop via {nh.nh} "+" encap seg6 mode inline segs {2} "+ f" weight {int(100/len(nhlist))} "
        self.add_command("0", f"ip -6 route add {{4}} metric 1 table 1 src {{0}}  {build_str}")
        # Demand from 1 to 5
        build_str = ""
        self.add_command("1", f"ip -6 route add {{5}} metric 1 table 1 src {{1}}  {build_str}")
        self.add_command("0", "ip -6 rule add to {5/} iif lo table 1")
        self.add_command("2", "ip -6 rule add to {3/} iif lo table 1")
        self.add_command("0", "ip -6 rule add to {4/} iif lo table 1")
        self.add_command("1", "ip -6 rule add to {5/} iif lo table 1")
        self.add_command("3", "nuttcp -6 -S")
        self.add_command("4", "nuttcp -6 -S")
        self.add_command("5", "nuttcp -6 -S")
        self.add_command("0", 'echo bash -c \\\"START=\\\\\$SECONDS\; while \! ip netns exec 0 nuttcp -T300 -i1 -R1000000000000 -N32 {5} \>\>flow_0-5.txt 2\>\&1 \; do sleep 1\; echo RTY\: \\\\\$SECONDS \>\>flow_0-5.txt\; done\\\" | at now+2min')
        self.add_command("2", 'echo bash -c \\\"START=\\\\\$SECONDS\; while \! ip netns exec 2 nuttcp -T300 -i1 -R1000000000000 -N32 {3} \>\>flow_2-3.txt 2\>\&1 \; do sleep 1\; echo RTY\: \\\\\$SECONDS \>\>flow_2-3.txt\; done\\\" | at now+2min')
        self.add_command("0", 'echo bash -c \\\"START=\\\\\$SECONDS\; while \! ip netns exec 0 nuttcp -T300 -i1 -R1000000000000 -N32 {4} \>\>flow_0-4.txt 2\>\&1 \; do sleep 1\; echo RTY\: \\\\\$SECONDS \>\>flow_0-4.txt\; done\\\" | at now+2min')
        self.add_command("1", 'echo bash -c \\\"START=\\\\\$SECONDS\; while \! ip netns exec 1 nuttcp -T300 -i1 -R1000000000000 -N32 {5} \>\>flow_1-5.txt 2\>\&1 \; do sleep 1\; echo RTY\: \\\\\$SECONDS \>\>flow_1-5.txt\; done\\\" | at now+2min')

        self.enable_throughput()
        self.add_command("0", "sysctl net.ipv6.fib_multipath_hash_policy=1")
        self.add_command("1", "sysctl net.ipv6.fib_multipath_hash_policy=1")
        self.add_command("2", "sysctl net.ipv6.fib_multipath_hash_policy=1")
        self.add_command("3", "sysctl net.ipv6.fib_multipath_hash_policy=1")
        self.add_command("4", "sysctl net.ipv6.fib_multipath_hash_policy=1")
        self.add_command("5", "sysctl net.ipv6.fib_multipath_hash_policy=1")

topos = {'apl': (lambda: apl())}

