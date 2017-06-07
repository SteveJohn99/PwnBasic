#!/usr/bin/env python
from pwn import *

# target
target = './bin'
target_bin = ELF(target)

# libc
libc_bin = ''

# process or remote instance
r = ''

# context
context.clear(arch=target_bin.arch)
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

# libc func
def libc_sym(sym):
    if libc_bin != None:
        return libc_bin.sym[sym]

def libc_str(s):
    if libc_bin != None:
        return libc_bin.search(s).next()

isRemote = False
isDebug  = True
isPTY = True

stdout = ''
stdin  = ''

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
    REMOTE = 'localhost'
    PORT   = 31337
    r = remote(REMOTE, PORT)
else:
    r = process(target, stdout=stdout, stdin=stdin)
    if isDebug:
        open("pid", "wb").write("%d\n"%r.pid)
        #gdb.attach(r, '''c''')
        #pause()

r.interactive()
