# Network Design Project – Phase Proposal & Design Document 
## (Phase 1 of 5)

**Team Name:**  N/A
**Members:** (Olivia Pham, olivia_pham@student.uml.edu)  
**GitHub Repo URL (with GitHub usernames):** https://github.com/olitranpham/network-design, olitranpham 
**Phase:** 1
**Submission Date:**  1/30/26
**Version:** v2

---

## Table of Contents

0. [Executive Summary](#0-executive-summary)
1. [Phase Requirements](#1-phase-requirements)
2. [Phase Plan](#2-phase-plan)
3. [Architecture and State Diagrams](#3-architecture-and-state-diagrams)
4. [Packet Format](#4-packet-format)
5. [Data Structures and Module Map](#5-data-structures-and-module-map)
6. [Protocol Logic](#6-protocol-logic)
7. [Experiments and Metrics Plan](#7-experiments-and-metrics-plan)
8. [Edge Cases and Test Plan](#8-edge-cases-and-test-plan)
9. [Repository Structure and Reproducibility](#9-repository-structure-and-reproducibility)
10. [Team Plan, Ownership, and Milestones](#10-team-plan-ownership-and-milestones)
11. [Demonstration Checklist](#11-demonstration-checklist)

---

## 0 Executive summary

**Phase 1(a):** UDP socket programming will be implemented with Python for a client and server, displaying bidirectional message transfer and an echo workflow. The first deliverable sends a "HELLO" message from the UDP client to the UDP server and echoes back to the client using different port numbers, although the client and server can run on the same machine. 

**Phase 1(b):** The second deliverable (Phase 1(b)) transfers a BMP image file from the client to server over UDP, while implementing the RDT 1.0 protocol. The sender will parse the BMP into fixed-size chunks and send one packet at a time, while the receiver reassembles packets in order and reconstructs the output BMP. Validation will be shown via a YouTube video plus a file-compare check. 

---

## 1 Phase Requirements

### 1.1 Demo Deliverable

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

### 1.2 Required Demo Scenarios

**Phase 1(a) - UDP Echo**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
| 1 - Client sends "HELLO" | Client bound to port 5000, server on port 5001, both sharing same host | Server receives "HELLO" messsage and echoes it back to client | Terminal with successful communication output |
| 2 - Bidirectional communication | Repeated message exchanges between client and server | Messages are successfully transmitted and echoed in both directions | Console log demonstrating multiple send/receive cycles |

**Phase 1(b) - RDT 1.0 File Transfer**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
| 1 - BMP file transfer | Transfer image.bmp using 1024-byte packets | Image file is successfully transmitted from sender to receiver | Terminal output showing packets being sent and received sequentially |
| 2 - File integrity verification | Compare original file with reconstructed file | File sizes and byte contents exactly match | Console output showing successful fire comparison |
| 3 - Visual confirmation | Open received file | Image displays correctly | Opening both original and received images |

### 1.3 Required Figures/Plots

N/A for Phase 1.

---

## 2 Phase Plan

### 2.1 Scope

**New behaviors added:** 
- Phase 1(a): UDP client sends "HELLO" message to server, server echoes message back to client
- Phase 1(b): BMP file is transferred from client to server using RDT 1.0 behavior -> input file is parsed and packetized into fixed sizes using make_packet function

**Behaviors unchanged from previous phase:** 
- No prior behaviors since this is the initial phase

**Out of scope (explicitly):**
- No implementation to handle packet loss or corruption

### 2.2 Acceptance Criteria 

**Phase 1(a):**
- [x] Client/server run via CLI with configurable ports.
- [x] "HELLO" is sent to client, sent and echoed to server, and sent back to client

**Phase 1(b):**
- [x] Select a BMP image file to transfer
- [x] Packetize the BMP image file
- [x] UDP sockets send and receive packets one file at a time
- [x] Receiver assembles packets in order and writes a complete output file in order
- [x] Receiver is delivered the entire transfer file

**General:**
- [x] README.md is complete
- [x] Invite instructor(s) to GitHub repo and include GitHub link
- [x] Record demo and upload to YouTube 

### 2.3 Work Breakdown

**Workstream A: Phase 1(a)**
- Create client.py function to send "HELLO" via UDP
- Create server.py function to echo "HELLO" back via UDP
- Test bidirectional communication

**Workstream B: Phase 1(b)**
- Create make_packet function
- Create parse_packet function
- Create sender/receiver file
- Compare input BMP file to output

**Workstream C: General**
- Complete file/function creation
- Record demos
- Complete/finalize documentation

---

## 3 Architecture and State Diagrams

### 3.1 State Diagram Evolution

#### Phase 1(a): UDP Echo

```
        UDP Server                               UDP Client
┌────────────────────────┐               ┌────────────────────────┐
│ Create UDP socket      │               │ Create UDP socket      │
└───────────┬────────────┘               └───────────┬────────────┘
            │                                        │
            ▼                                        ▼
┌────────────────────────┐     "HELLO"    ┌───────────────────────┐
│ Bind to server port    │◄─────sent──────│ Bind to client port   │
│ and wait for message   │                │ and send datagram     │
│                        │                │ to server IP:port     │
└───────────┬────────────┘                └───────────────────────┘
            │ Message received                         ▲
            ▼                                          │
┌────────────────────────┐     Echo       ┌────────────┴───────────┐
│ Send received message  │─────sent──────►│ Receive echoed message │
│ back to client using   │                │ on client socket       │
│ server socket          │                │                        │
└────────────────────────┘                └───────────┬────────────┘
                                                       │ Message received
                                                       ▼
                                            ┌────────────────────────┐
                                            │ Close client socket    │
                                            └────────────────────────┘
```
#### Phase 1(b): RDT 1.0 File Transfer

**Sender State Machine:**

```
    +----------------------------------+
    |  Wait for file data from sender  |<----+
    +----------------------------------+     |
                 |                           |
                 | for each chunk            |
                 v                           |
    +----------------------------------+     |
    | packet = make_packet(seq, data,  |     |
    |           total_packets)         |     |
    | socket.sendto(packet)            |     |
    +----------------------------------+     |
                 |                           |
                 +---------------------------+
```

**Transition Conditions:**
- Triggered by: Sender reading the next file chunk in the send loop
- Action: Create a packet using `make_packet(seq, chunk, total_packets)` and transmit it with `socket.sendto()`
- Next state: Wait for the next file chunk (or terminate after the final packet is sent)

**Receiver State Machine:**

```
    +----------------------------------+
    |  Listen for incoming UDP packet  |<----+
    +----------------------------------+     |
               |                             |
               | recvfrom()                  |
               v                             |
    +----------------------------------+     |
    | parse_packet()                   |     |
    | packets[seq] = payload           |     |
    +----------------------------------+     |
               |                             |
               +-----------------------------+
```

**Transition Conditions:**
- Triggered by: Arrival of a UDP packet on the receiving socket via socket.recvfrom()
- Action: Parse the packet using `parse_packet()`, store the payload at `packets[seq]`, and update the received packet count
- Next state: Wait for the next packet (or terminate once `received_count == total_packets`)

### 3.2 Component Responsibilities

**Sender Components**

`client.py` (Phase 1(a)) - Main responsibilities:
- Create a UDP socket for the client
- Send the fixed message "HELLO" to the server
- Receive the echoed response from the server
- Display the received message and close the socket

`sender.py` (Phase 1(b)) - Main responsibilities:
- Read BMP into memory
- Compute the total number of packets using a fixed payload size
- Divide BMP file data into chunks of 1024 bytes
- Create packets using `make_packet(seq, payload, total_packets)`
- Send packets one at a time to the receiver using UDP
- Print transmission progress into console

**Receiver Components**

`server.py` (Phase 1(a)) - Main responsibilities:
- Create and bind a UDP socket to the server port
- Listen for incoming UDP messages
- Print received message into console
- Echo received messages back to the clinet

`receiver.py` (Phase 1(b)) - Main responsibilities:
- Create and bind UDP socket to the specified port
- Receive incoming packets from sender
- Parse packets using `parse_packet()` to extract sequence number and payload
- Store payloads in a buffer indexed by sequence number
- Track the number of packets received
- Detect transfer completion when `received_count == total packets`
- Reassemble the original file in sequential order
- Write the reconstructed file to disk

**Shared Modules**
- `make_packet.py` - Packet encoding/decoding utilities
	- `make_packet(seq, payload, total_packets)` encodes packet header fields and payload into a byte stream
- `parse_packet(data)` decodes received packet bytes into `(sequence_number, payload, total_packets)`

### 3.3 Message Flow Overview

**Phase 1(a) - UDP Echo**

```
[client] --["HELLO"]-> [server]
[client] <-["HELLO"]-- [server]
```

**Phase 1(b) - RDT 1.0 File Transfer**

```
[input.bmp] -> sender -> UDP port -> receiver -> [output.bmp]
```

---

## 4 Packet Format

### 4.1 Packet Types
- DATA: carries chunks of BMP file
- END: indicates end of file transfer

### 4.2 Header Fields

| Field | Size (bytes/bits) | Type | Description | Notes |
|---|---:|---|---|---|
| seq | 4 | uint32 | Packet sequence number | Used by receiver to place payloads in correct order |
| payload_length | 4 | uint32 | Payload length in bytes | Allows last packet to be smaller than 1024 bytes |
| total_packets | 4 | uint32 | Detects transfer completion |  
| payload | ≤ 1024 | bytes | File data chunk | Binary-safe |

**Total header size:** 12 bytes
**Maximum packet size:** 12 + 1024 = 1036 bytes

**Encoding format (Python struct):**
```python
# Network byte order (big-endian)
header_format = "!III"  # 3 unsigned 32-bit integers
```

---

## 5 Data Structures and Module Map

### 5.1 Key Data Structures

**Packet Structure** (in `make_packet.py`)

- Fields:
  - `seq` (uint32): Sequence number of the packet, starting at 0
  - `payload_length`(uint32): Number of valid bytes in the payload
  - `total_packets` (uint32): Total number of packets in the transfer
  - `payload` (bytes): File data chunk (up to 1024 bytes)

- Invariants:
  - `0 <= seq < total_packets`
  - `1 <= payload_length <= 1024`
  - `total_packets >= 1`

**Sender File Buffer** (in `sender.py`)

- Fields:
  - `file_data` (bytes): Entire input file read into memory
  - `file_size` (int): Total size of the input file in bytes
  - `total_packets` (int) - Number of packets required to send the file

- Invariants:
  - `file_size == len(file_data)`
  - `total_packets == (file_size + MAX_PAYLOAD - 1) // MAX_PAYLOAD`
  - Each packet payload size is <= 1024 bytes

**Receiver Packet Buffer** (in `receiver.py`)

- Fields:
  - `packets` (list): List of packet payloads indexed by `seq`
  - `total_packets` (int): Expected total number of packets (from first received packet)
  - `received_count` (int): Number of packets successfully received

- Invariants:
  - `len(packets) == total_packets`
  - `received_count <= total_packets`
  - Each payload is written at index `packets[seq]`
  - Transfer is complete when `received_count == total_packets`

### 5.2 Module Map and Dependencies

```
src/
|-- client.py       # Phase 1(a): UDP echo client sends "HELLO"
|-- server.py       # Phase 1(a): UDP echo server (echoes received message)
|-- sender.py       # Phase 1(b): RDT 1.0 file sender
|-- receiver.py    	# Phase 1(b): RDT 1.0 file receiver
|-- make_packet.py  # Packet encode/decode utilities
```

**Dependency Graph:**

```
client.py  	  	 -> socket
server.py   	 -> socket

sender.py  		 -> socket, argparse, make_packet.py
receiver.py 	 -> socket, argparse, make_packet.py

make_packet.py   -> struct
```

## 6 Protocol Logic 

### 6.1 Sender Behavior

**Phase 1(a) - UDP Client Logic**

Steps:
1. Create UDP socket
2. Send "HELLO" to server
3. Print received message

**Phase 1(a) Pseudocode:**

```
initialize sequence_number = 0

while true do
    read up to 1024 bytes from input file into chunk
    if chunk is empty then
        break
    end if

    packet ← make_packet(sequence_number, chunk, total_packets)
    send packet over UDP socket

    sequence_number ← sequence_number + 1
end while

send final END packet over UDP socket
```

**Phase 1(b) - RDT 1.0 Sender Logic**

Steps:
1. Open input BMP in binary
2. Loop
	- Read up to 1024 bytes
	- Create DATA packet with seq, len, and payload
	- Send packet over UDP
	- Increment seq
3. Close socket
	
**Phase 1(b) Sender Pseudocode:**

```
set seq to 0

repeat
    read next 1024-byte block from file into chunk
    if no data was read then
        exit loop
    end if

    create DATA packet with:
        sequence number = seq
        payload length = size of chunk
        payload = chunk

    send packet using UDP
    increment seq
until end of file reached

create END packet with:
    sequence number = seq
    payload length = 0

send END packet using UDP
```

### 6.2 Receiver Behavior

**Phase 1(a) - UDP Server Logic**
Steps:
1. Bind UDP socket to server port
2. Receive "HELLO" from sender
3. Echo message back to sender address

**Phase 1(a) Pseudocode:**

```
initialize UDP server socket
bind socket to server port

print "server is ready to receive"

while true do
    receive message and client address from UDP socket
    display received message
    send the same message back to the client
end while
```

**Phase 1(b) - RDT 1.0 Receiver Logic**
Steps:
1. Bind UDP socket to server port
2. Open output BMP
3. Loop:
	- Receive UDP data
	- Parse header
	- If END: break
	- If DATA: Accept in sequential order
4. Close socket

**Phase 1(b) Receiver Pseudocode:**

```
initialize UDP socket
bind socket to receiver port

initialize total_packets to null
initialize packets buffer to empty
initialize received_count to 0

while true do
    receive packet from UDP socket
    parse packet to extract seq, payload, and total_packets

    if total_packets is null then
        set total_packets from packet header
        initialize packets buffer with size total_packets
    end if

    if packets[seq] is empty then
        store payload in packets[seq]
        increment received_count
        display receive progress
    end if

    if received_count equals total_packets then
        break
    end if
end while

reassemble file by concatenating packets in sequence order
write reconstructed file to output
close UDP socket
```

### 6.3 Error / Loss Injection Specification

Not implemented in Phase 1. RDT 1.0 assumes a perfectly reliable channel.

---

## 7 Experiments and Metrics Plan

Phase 1 does not require performance metrics, timing measurements, or plots.

**Output Artifacts:**
- Console logs showing packet transmission progress
- Transferred file saved to `results/` directory

---

## 8 Edge Cases and Test Plan

### 8.1 Expected Edge Cases

| Edge case | Why it matters | Expected behavior |
|---|---|---|
| last packet smaller than payload size | correct file reconstruction | receiver writes exact bytes |
| duplicate packets/ACKs | protocol correctness | ignored or re-ACKed |
| corrupted header | checksum coverage | drop / request retransmit |
| termination marker handling | clean shutdown | no deadlocks |

### 8.2 Tests
- `test_make_parse_roundtrip`: `make_packet(seq, payload, total)` then `parse_packet()` returns the same `seq`, `payload`, and `total`
- `test_max_payload_1024`: payload of exactly 1024 bytes encodes/decodes correctly
- `test_small_payload`: payloads of less than 1024 bytes encodes/decodes correctly

**Integration Tests:**
- `test_udp_echo_hello`: run `server.py` and `client.py`, verify that the received message is "HELLO"
-`test_transfer_bmp`: run `receiver.py` and `sender.py` with BMP image file, verify output file opens correctly and matches input byte-for-byte

### 8.3 Test Artifacts

- Console logs saved to `results/logs/`
- Output files from tests in `results/`
- Test scripts in `tests/`

---

## 9 Repository Structure and Reproducibility

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

**To reproduce:**
```
:: Terminal 1 – Start receiver
python receiver.py --port 9000 --output received.bmp

:: Terminal 2 – Start sender
python sender.py --host 127.0.0.1 --port 9000 --file image.bmp
```

---

## 10 Team Plan, Ownership, and Milestones

### 10.1 Task Ownership

| Task | Owner | Target Date | Definition of Done |
|---|---|---|---|
| UDP client/server (1a) | Self | 1/30/26 | Client sends "HELLO" and server echoes it back successfully |
| Packet encode/decode | Self | 1/30/26 | `make_packet()` and `parse_packet()` correctly encode/decode packets |
| Sender logic (1b) | Self | 1/30/26 | `sender.py` sends all file packets sequentially over UDP |	
| Receiver logic (1b) | Self | 1/30/26 | `receiver.py` reassembles the file correctly from received packets |
| Integration testing | Self | 1/30/26 | File transfer completes and output file matches input |
| Demo video | Self | 1/30/26 | Video demonstrates Phase 1(a) and Phase 1(b) successfully |
| Documentation | Self | 1/30/26 | Design document and README completed and submitted |

### 10.2 Milestones

1. **M1:** Phase 1(a) complete –> UDP client sends `"HELLO"` and server echoes response  
2. **M2:** Packet utilities complete –> `make_packet()` and `parse_packet()` validated  
3. **M3:** Sender complete –> file packetized and sent sequentially over UDP  
4. **M4:** Receiver complete –> packets received and file reassembled correctly  
5. **M5:** End-to-end transfer verified –> received file matches original  
6. **M6:** Submission ready –> demo video recorded and documentation finalize

---

## 11 Demonstration Checklist

### Pre-Recording Checklist

**Phase 1(a):**
- [x] Server starts successfully on specified port
- [x] Client sends "HELLO" message
- [x] Server receives and displays message
- [x] Server echoes message back
- [x] Client receives and displays echoed message

**Phase 1(b):**
- [x] Receiver starts and listens on specified port
- [x] Sender reads BMP file successfully
- [x] Packet transmission shows progress (seq/total)
- [x] All packets received (receiver shows count)
- [x] File saved to output directory
- [x] Both BMP files open and display correctly

**Video Quality:**
- [x] Both terminal windows visible side-by-side
- [x] Clear explanation of steps
- [x] Show file comparison/verification


