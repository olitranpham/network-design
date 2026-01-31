# Network Design Project – Olivia Pham

## Overview

## Team
| Name | Email | Primary responsibility |
|---|---|---|
| Olivia Pham | olivia_pham@student.uml.edu | Entire project |

## Demo Video

- **Private YouTube link - Phase 1(a)** 
	- Link: https://youtu.be/g8XUVhSGN4Q
		- Timestamped outline:
			- 0:00-0:04 -> UDP server initialized and waiting for incoming message
			- 0:04-0:11 -> UDP client sends "HELLO" to server, server receives message and echoes back to client

- **Private YouTube link - Phase 1(b)** 
	- Link: https://youtu.be/gzKlD03q-Sw
		- Timestamped outline:
			- 0:00-0:02 -> Showing original BMP image file in folder  
			- 0:02-0:05 -> Initializing receiver.py
			- 0:05-0:11 -> Sender (right) sending 1024-byte packets sequentially, and receiver (left) receives and reassembles all 157 packets successfully
			- 0:11-0:32 -> comparing original BMP file with received/new file

---

## Repository Structure (required)
Your repo must match this layout (minimum):

```
project/
|-- src/
|   |-- client.py          # Phase 1(a): UDP echo client
|   |-- server.py          # Phase 1(a): UDP echo server
|   |-- sender.py          # Phase 1(b): RDT 1.0 sender
|   |-- receiver.py        # Phase 1(b): RDT 1.0 receiver
|   |-- make_packet.py     # Packet encode/decode
|
|-- tests/
|   |-- test_packet.py     # Unit tests for packet module
|   |-- test_transfer.py   # Integration tests
|
|-- scripts/
|   |-- run_demo.sh        # Demo script
|
|-- test_files/
|   |-- test.bmp           # Test input file
|
|-- results/
|   |-- (output files)
|
|-- docs/
|   |-- DESIGN_DOC.md      # This document
|
|-- README.md
```

## Requirements
- Language/runtime: Python 3.14.2
- OS tested: Windows
- Dependencies:
  - Python: `pip install -r requirements.txt`

---

## Standard CLI Interface 

### Receiver (required flags)
- `--port <int>`: UDP port to bind
- `--out <path>`: output file path to write received bytes
- `--seed <int>`: RNG seed (default: 0)
- `--log-level <debug|info|warning|error>` (default: info)

### Sender (required flags)
- `--host <ip/hostname>`: receiver host
- `--port <int>`: receiver port
- `--file <path>`: input file to send
- `--seed <int>`: RNG seed (default: 0)
- `--log-level <debug|info|warning|error>` (default: info)

### Injection Flags

N/A for Phase 1. 

### Timing / Windowing Flags

N/A for Phase 1.

**Notes**
- “Rates” are probabilities per packet/ACK.
- Timing experiments must disable verbose logging (use `--log-level warning` or `error`).

---

## Quick Start (Run Locally)

```
:: Terminal 1 – Start receiver
python receiver.py --port 9000 --output received.bmp

:: Terminal 2 – Start sender
python sender.py --host 127.0.0.1 --port 9000 --file image.bmp
```

---

## Required Demo Scenarios
Provide the exact commands used to demonstrate each required scenario.

### Scenario 1: Phase 1(a) - UDP Echo

Server:
```cmd
python server.py
```

Client:
python `client.py`

Expected behavior:
- Server starts and listens on the configured UDP port
- Client sends the message "HELLO" to the server
- Server receives and echoes "HELLO" back to the client
- Client prints the echoed message and exits successfully

### Scenario 2: Phase 1(b) - RDT 1.0 File Transfer

Receiver:
```cmd
python receiver.py --port 9000 --output received.bmp
```

Sender:
```cmd
python sender.py --host 127.0.0.1 --port 9000 --file image.bmp
```

Expected behavior:
- Receiver starts and listens on the specified UDP port
- Sender reads the input file and packetizes it into 1024-byte chunks
- Packets are sent sequentially over UDP using RDT 1.0 
- Receiver receives all packets, reassembles them in order, and writes the output file
- Transfer completes when all packets are received
- The reconstructed file (`received.bmp`) matches the original file (`image.bmp`)

## Figures / Plots 

N/A for Phase 1. 

### Results files
- `results/output.bmp`

---

## Known Issues / Limitations

N/A for Phase 1.

---

## Academic Integrity / External Tools
Debugging tools (IDE debugger, logging) and LLMs may be used for learning and troubleshooting. Final implementation decisions and understanding are our own.

