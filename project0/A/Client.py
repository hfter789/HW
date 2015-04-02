import threading
import sys
import socket
import base64
import time
import Queue
import random
import select
from sys import stdin
from threading import Timer

HELLO,DATA,ALIVE,BYE = range(4)
COMMAND = ['HELLO','DATA','ALIVE','BYE']
TIMEOUT = 5.0
MAGIC = 'C461'
VERSION = 1


def main():
	if(len(sys.argv)!=3):
		print "Not Enough Arguments"
		return;
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])

	cmdQ = Queue.Queue()
	cmdQ.put((HELLO,None))
	alive = threading.Event()
	t = ClientThread(cmdQ,alive,HOST,PORT)
	t.start()
	running = True;

	while (running):
		try:
			while sys.stdin in select.select([sys.stdin], [], [], TIMEOUT)[0]:
				input = sys.stdin.readline()
				if len(input)==0:
					if cmdQ.empty():
						running = False 
						break
				else:
					cmdQ.put((DATA,input))
			else:
				if not alive.isSet():
					break
		except KeyboardInterrupt:
			break

	t.join()
	exit()

class ClientThread(threading.Thread):
	def __init__(self, commandQ, alive, targetHost='127.0.0.1', targetPort=3333, listenHost = '127.0.0.1',listenPort = 1234):
		super(ClientThread, self).__init__()
		self.commandQ = commandQ or Queue.Queue()
		self.alive = alive
		self.alive.set()
		self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
		# self.socket.bind(('',listenPort))
		self.packetSent = 0;
		self.targetAddr = (targetHost,targetPort)
		self.ID = base64.b16decode(hex(random.randint(0,4294967295))[2:10].zfill(8),True)
		self.timer = None
		self.socket.settimeout(1.0)
		self.lock = threading.Lock()

	def closeClient(self, notify = False):
		#close the client, if notify is true, client will send GOODBYE to the server
		#and wait for response with a TIMEOUT.
		#after that, the thread alive flag is set to false by calling clear()
		#and timer is cancel if there is one
		if notify and self.alive.isSet():
			self.sendMessage(BYE,None)
			self.recvMessage(BYE,TIMEOUT)
		self.alive.clear()
		if(self.timer is not None):
			self.timer.cancel()

		# print "Finshed closeClient"

	def run(self):
		while self.alive.isSet():
			# print "inloop"
			try:
				#block 0.1 sec
				cmd = self.commandQ.get(True, 0.1)
				#cmd[0] is the command, cmd[1] is data(could be None)
				self.sendMessage(cmd[0],cmd[1])
				if self.timer is None:
					self.timer = Timer(TIMEOUT, self.closeClient, [True])
					self.timer.start()
				#command ALIVE would not expect any response from server
				if cmd[0] == ALIVE:
					continue
				#wait for response from server
				while self.alive.isSet():
					if self.recvMessage(cmd[0]):
						break
			except Queue.Empty as e:
				if self.alive.isSet():
					self.recvMessage()

	def recvMessage(self,command=None,timeout = 1.0):
		self.socket.settimeout(timeout)
		try:
			response,address = self.socket.recvfrom(128)
			return self.processResponse(response,address,command)
		except socket.timeout:
			# print "Timeout!"
			return False

	def processResponse(self, response, address, command):

		# print response[0:2].encode('hex').upper() != MAGIC
		# print int(response[2].encode('hex')) != VERSION
		# print response.encode('hex')
		if (response[0:2].encode('hex').upper() != MAGIC) or (int(response[2].encode('hex')) != VERSION):
			# print "not valid"
			return False;
		resp = int(response[3].encode('hex'))
		# print
		# if(command is None):
		# 	print "Sent ", None
		# else:
		# 	print "Sent ", COMMAND[command]
		# print "Received ", COMMAND[resp]
		if (command == HELLO and int(resp) == HELLO) or (command == DATA and resp == ALIVE):
			#valid response, reset timer
			self.timer.cancel()
			self.timer = None
			return True
		#close the client if received GOODBYE from the server
		if(resp == BYE and command == BYE):
			return True
		if(resp == BYE):
			self.closeClient()
			return True
		return False

	def sendMessage(self, cmd, data):
		self.lock.acquire()
		#contruct the protocol
		message = base64.b16decode(b'C46101')
		# command is 1 byte fill empty space with 0
		message += base64.b16decode(str(cmd).zfill(2))
		# the # of packets sent is 4 bytes, convert it to hext,
		# and fill the empty with 0
		message += base64.b16decode(hex(self.packetSent)[2:10].zfill(8),True)
		message += self.ID
		#print message.encode('hex')
		#append data if cmd is DATA
		if(data and cmd == 1):
			message += data

		# if self.socket
		self.socket.sendto(message, self.targetAddr)
		self.packetSent += 1
		# self.commandQ.task_done()
		self.lock.release()

	def join(self, timeout=None):
		#wait until the command Q is clear
		self.closeClient(True)
		# self.alive.clear()
		self.socket.close()
		# print 'socket close'
		threading.Thread.join(self, timeout)
		# print "thread Done"
		

if __name__ == '__main__':
	main()
