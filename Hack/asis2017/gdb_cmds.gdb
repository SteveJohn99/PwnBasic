#added this Python snippet: gdb_cmds.gdb
set disable-randomization off
catch exec
r

# Hit exec catchpoint

# Set breakpoints

#break *0x400960


# Continue executing (until we hit a breakpoint)
c
