#added this Python snippet: gdb_cmds.gdb
set disable-randomization off
catch exec
r

# Hit exec catchpoint

# Set breakpoints

break vulnerable_function


# Continue executing (until we hit a breakpoint)
c
