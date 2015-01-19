import threading
import sys
import socket
import base64
import time
import Queue
import random
from sys import stdin
from threading import Timer

HELLO,DATA,ALIVE,BYE = range(4)
TIMEOUT = 5.0
MAGIC = 'C461'
VERSION = 1


def main():
	if(len(sys.argv)!=3):
		print "Not Enough Arguments"
		return;
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	# sock.bind(('127.0.0.1',1234))

	cmdQ = Queue.Queue()
	cmdQ.put((HELLO,None))
	rplyQ = Queue.Queue()
	t = ClientThread(cmdQ,rplyQ,HOST,PORT)
	t.start()
	running = True;

	while(running):
		# try:
		input = stdin.readline()
		if(input == 'q' or input == 'q\n' or input ==''):
			running = False
			cmdQ.put((BYE,None))
		else:
			#everything else is data
			cmdQ.put((DATA,input))
		# except (KeyboardInterrupt,SystemExit):
		# 	running = False
		# 	cmdQ.put((BYE,None))
		# 	t.join(2)
		# 	print 'done'
		# 	exit()

	# cmdQ.join()
	t.join(2)
	exit()

class ClientThread(threading.Thread):
	def __init__(self, commandQ, replyQ, targetHost='127.0.0.1', targetPort=3333, listenHost = '127.0.0.1',listenPort = 1234):
		super(ClientThread, self).__init__()
		self.commandQ = commandQ or Queue.Queue()
		self.replyQ = replyQ or Queue.Queue()
		self.alive = threading.Event()
		self.alive.set()
		self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
		# self.socket.bind(('',listenPort))
		self.packetSent = 0;
		self.targetAddr = (targetHost,targetPort)
		self.ID = base64.b16decode(hex(random.randint(0,4294967295))[2:10],True)
		self.timer = None
		self.socket.settimeout(TIMEOUT)

	def closeClient(self):
		self.commandQ.put((BYE,None))
		self.alive.clear()
		if(self.timer is not None):
			self.timer.cancel()

	def run(self):
		while self.alive.isSet():
			# print "inloop"
			try:
				#block 0.1 sec
				cmd = self.commandQ.get(True, 0.1)
				#cmd[0] is the command, cmd[1] is data(could be None)
				self.sendMessage(cmd[0],cmd[1])
				self.timer = Timer(TIMEOUT, self.closeClient)
				#command ALIVE would not expect any response from server
				if cmd[0] == ALIVE:
					continue
				while self.alive.isSet():
					try:
						response,address = self.socket.recvfrom(128)
						if self.processResponse(response,address,cmd[0]) is True:
							break;
					except socket.timeout:
						print "Timeout!"
						self.closeClient()
						continue
			except Queue.Empty as e:
				continue

	def processResponse(self, response, address, command):

		# print response[0:2].encode('hex').upper() != MAGIC
		# print int(response[2].encode('hex')) != VERSION
		
		if (response[0:2].encode('hex').upper() != MAGIC) or (int(response[2].encode('hex')) != VERSION):
			print "not valid"
			return False;
		resp = int(response[3].encode('hex'))
		if (command == HELLO and int(resp) == HELLO) or (command == DATA and resp == ALIVE) or \
		(command == BYE and resp ==BYE):
			#valid response, reset timer
			self.timer.cancel()
			self.timer = None
			return True

	def sendMessage(self, cmd, data):
		#contruct the protocol
		message = base64.b16decode(b'C46101')
		# command is 1 byte fill empty space with 0
		message += base64.b16decode(str(cmd).zfill(2))
		# the # of packets sent is 4 bytes, fill the empty with 0
		message += base64.b16decode(str(self.packetSent).zfill(8))
		message += self.ID
		print message.encode('hex')
		#append data if cmd is DATA
		if(data and cmd == 1):
			message += data

		self.socket.sendto(message, self.targetAddr)
		self.packetSent += 1
		self.commandQ.task_done()

	def join(self, timeout=None):
		#wait until the command Q is clear
		# self.commandQ.join()
		self.alive.clear()
		self.socket.close()
		threading.Thread.join(self, timeout)
		print "thread Done"
		

if __name__ == '__main__':
	main()