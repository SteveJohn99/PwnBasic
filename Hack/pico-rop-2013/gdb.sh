#!/bin/bash

GDB_CMD_FILE="gdb_cmds.gdb"

pkill socat


# Be verbose
set -e

function usage {
    echo "Usage: $0 (debug|d)|(run|r) BINARY"
    exit 1
}

if [[ $# -ne 2 ]]; then
    usage
fi

# Get absolute address
BINARY="$(readlink -f "$2")"
BIN_DIR="$(dirname "${BINARY}")"
BIN_NAME="$(basename "${BINARY}")"

# Change working directory to binary's dir
ORIGINAL_WD="$(pwd)"
cd "${BIN_DIR}"

CMD="socat TCP4-LISTEN:40645,bind=127.0.0.1,reuseaddr EXEC:./${BIN_NAME}"
#CMD="socat TCP4-LISTEN:2600,bind=127.0.0.1,fork,reuseaddr EXEC:\"strace -if ./${BIN_NAME}\""
GDB_CMD_FILE=${ORIGINAL_WD}/${GDB_CMD_FILE}

case "$1" in
d|debug)
	echo "[*] cheese, socat with gdb setting"
	echo "[*] bind : localhost / listen : 40645"
    gdb -q -x ${GDB_CMD_FILE} --args $CMD
    ;;
r|run)
	echo "[*] cheese, socat setting"
	echo "[*] bind : localhost / listen : 40645"
    $CMD
    ;;
*)
    echo "[-] Invalid command"
    usage
    ;;
esac

~
