def pkt_callback(x):
	if 'Raw' in x:
		r = (x[Raw].load).split(',')
		state = r[1]
		print "state : %s" % state

#maybe you should change ip and port with yours?
#scapy.sniff(iface='wlp8s0', prn=pkt_callback, filter='tcp and host 192.168.0.26 and port 50583', store=0)
