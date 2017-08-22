gcc -fno-stack-protector -m32 -z execstack -O0 -o $1 $1.c
