section	.text
	global _start       ;must be declared for using gcc
_start:                     ;tell linker entry point
    mov edi, msg
	mov	edx, cs;8;len    ;message length
	mov	ecx, edi    ;message to write
	mov	ebx, 1	    ;file descriptor (stdout)
	mov	eax, 4	    ;system call number (sys_write)
	add ecx, eax
	int	0x80        ;call kernel
	mov	eax, 1	    ;system call number (sys_exit)
	int	0x80        ;call kernel

section	.data

msg	db	'Hello, world!',0xa	;our dear string
len	equ	$ - msg			;length of our dear string
