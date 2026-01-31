#!/bin/bash
set -e

# Phase 1(a): UDP echo
python src/server.py &
SPID=$!
sleep 1
python src/client.py
kill $SPID 2>/dev/null || true

# Phase 1(b): RDT 1.0 file transfer
mkdir -p results
python src/receiver.py --port 9000 --output results/received.bmp &
RPID=$!
sleep 1
python src/sender.py --host 127.0.0.1 --port 9000 --file test_files/test.bmp
wait $RPID
