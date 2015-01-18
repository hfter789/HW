import threading
import sys
import socket
import base64
import time
import Queue
import random
from sys import stdin

def main():
	if(len(sys.argv)!=3):
		print "Not Enough Arguments"
		return;
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])

	cmdQ = Queue.Queue()
	cmdQ.put((0,None))
	rplyQ = Queue.Queue()
	t = ClientThread(cmdQ,rplyQ,HOST,PORT)
	t.start()
	running = True;

	while(running):
		input = stdin.readline()
		if(input == 'q' or input == 'q\n'):
			running = false
			cmdQ.put((3,None))
		else:
			#everything else is data
			cmdQ.put((1,input))
	
	# message = base64.b16decode(b'C4610100000000001B2D3C4A')

	# sock.sendto(message, (HOST, PORT))

	# message = base64.b16decode(b'C4610101000000011B2D3C4A')
	# message += "Message"

	# print message

	# sock.sendto(message, (HOST, PORT))

class ClientThread(threading.Thread):
	def __init__(self, commandQ, replyQ, HOST, PORT):
		super(ClientThread, self).__init__()
		self.commandQ = commandQ or Queue.Queue()
		self.replyQ = replyQ or Queue.Queue()
		self.alive = threading.Event()
		self.alive.set()
		self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
		self.socket.bind(('127.0.0.1',1234))
		self.packetSent = 0;
		self.HOST = HOST
		self.PORT = PORT
		self.ID = random.randint(0,4294967296)

	def run(self):
		while self.alive.isSet():
			try:
				cmd = self.commandQ.get()
				self.sendMessage(cmd[0],cmd[1])
			except Queue.Empty as e:
				continue

	def sendMessage(self, cmd, data):
		#contruct the protocol
		message = base64.b16decode(b'C46101')
		cmd = base64.b16decode(str(cmd).zfill(2))
		seqNum = base64.b16decode(str(self.packetSent).zfill(8))
		seqID = base64.b16decode(str(self.ID).zfill(8))

		message += cmd + seqNum + seqID
		if(data):
			message += data
		self.socket.sendto(message, (self.HOST, self.PORT))

	def join(self, timeout=None):
		self.alive.clear()
		self.socket.close()
		threading.Thread.join(self, timeout)



if __name__ == '__main__':
	main()