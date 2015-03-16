import socket
from sys import *
import base64
import threading

BUF_SIZE = 8
ROUND = 10
TIMEOUT = 1
CMD = {
	'PIK':1, #tells everyone that I want to pick this time, no response needed
	'REQ':2,	#tells everyone that I want to decide on this time, a NAK would cancel it
	'NAK':3, #tells the sender that you can't take this time
}

def getGroups(fileName):
	with open(fileName) as f:
		content = f.readlines()
	group = []
	for l in content:
		l = l.strip('\n')
		tokens = l.split()
		if len(tokens) == 2:
			group.append((tokens[0],int(tokens[1])))
	return group
# helper
def intToBytes(num, numOfBytes):
  #take the hex, remove '0x', fill the empty spot with 0
  #and convert
  if not num:
    num = 0
  try:
    return base64.b16decode(hex(num)[2:].zfill(numOfBytes*2),True)
  except :
  	pass

def makeMsg(cmd, k):
	return intToBytes(cmd, 4)+intToBytes(k,4)

def receiver(sock, mypref):
	while True:
		try:
			data, addr = sock.recvfrom(BUF_SIZE)
		except socket.timeout:
			continue
		except:
			#error
			return
		cmd = int(data[:4].encode('hex'),base=16)
		pref = int(data[4:].encode('hex'),base=16)
		if cmd == CMD['REQ']:
			if pref != mypref:
				sock.sendto(makeMsg(CMD['NAK'],mypref),addr)


def main():
	fileName = argv[1]
	port = int(argv[2])
	pref = int(argv[3])
	group = getGroups(fileName)
	N = len(group)
	# print group
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('127.0.0.1',port))
	resolve = False
	round = 0
	rec = {}
	while round < ROUND:
		for addr in group:
			sock.sendto(makeMsg(CMD['PIK'],pref), addr)
		sock.settimeout(TIMEOUT)
		for _ in range(N):
			try:
				data, addr = sock.recvfrom(BUF_SIZE)
			except socket.timeout:
				break
			# recordData(rec,data)
			cmd = int(data[:4].encode('hex'),base=16)
			pref = int(data[4:].encode('hex'),base=16)
			if cmd == CMD['PIK']:
				if data in rec:
					rec[pref] += 1
				else:
					rec[pref] = 1
		k = 0
		for key in rec:
			if rec[key] > k:
				k = rec[key]
				pref = key
		round += 1
		rec = {}
		if round == ROUND:
			#Do a REQ
			for addr in group:
				sock.sendto(makeMsg(CMD['REQ'],pref), addr)
			for _ in range(N):
				try:
					data, addr = sock.recvfrom(BUF_SIZE)
				except socket.timeout:
					break
				cmd = int(data[:4].encode('hex'),base=16)
				pref = int(data[4:].encode('hex'),base=16)
				#if there is a NAK, redo the selection again
				if cmd == CMD['NAK']:
					# print "Got a NAK"
					round = 0
					continue
	print pref
	mypref = pref
	#after printing my time, I will keep sending my pref to everyone
	#so take over their rec map
	#if I receive a REQ of a pref number that's not equal to mine, I NAK(refuse) it
	t = threading.Thread(target = receiver, args = (sock,mypref))
	t.setDaemon(True)
	t.start()
	while True:
		for addr in group:
			try:
				sock.sendto(makeMsg(CMD['PIK'],mypref), addr)
			except:
				return


if __name__ == '__main__':
	main()