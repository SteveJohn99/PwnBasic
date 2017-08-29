#added this Python snippet: gdb_cmds.gdb
#set environment LD_PRELOAD=./libc.so.6
#set disable-randomization off
set disable-randomization off
catch exec
r


# Set breakpoints

break *level

#break level+252



# Continue executing (until we hit a breakpoint)
c
