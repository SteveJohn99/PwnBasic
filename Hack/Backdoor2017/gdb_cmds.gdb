#added this Python snippet: gdb_cmds.gdb
set disable-randomization off
set exec-wrapper env 'LD_PRELOAD=libc.so.6'
#set environment LD_PRELOAD='./libc.so.6'
catch exec
r

# Hit exec catchpoint

# Set breakpoints

break *main+60


# Continue executing (until we hit a breakpoint)
c
