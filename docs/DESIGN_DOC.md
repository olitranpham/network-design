# Network Design Project – Phase Proposal & Design Document 
## (Phase 2 of 5)

**Team Name:**  Don't Be COI

**Members:** 
- Cody Nguyen: cody_nguyen@student.uml.edu
- Olivia Pham: olivia_pham@student.uml.edu
- Ian Khoo: ian_khoo@student.uml.edu

**GitHub Repo URL (with GitHub usernames):** https://github.com/olitranpham/network-design, olitranpham 

**Phase:** 2

**Submission Date:**  2/13/26

**Version:** v3

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

**Phase 2(a):** Implement RDT2.2 over UDP for reliable delivery under bit errors. The protocol will use sequence numbers, checksums, and ACK packets so the sender only moves on after receiving a valid ACK from the current sequence number.

**Phase 2(b):** Add required bit-error injection scenarios to demonstrate order under corruption.
	- Option 1: No loss/bit-errors.
	- Option 2: Corrupt ACK packets where sender can detect invalid ACK and retransmits the last DATA packet.
	- Option 3: DATA bit-error where receiver detcts corruption and sends the last valid ACK, allowing for sender retransmission. 

**Phase 2(c):** Run a performance evaluation by measuring completion time over impairment rate from 0% to 95% in 5% increments, taking the average of 5 runs per impairment level, and generating the required plots. 

---

## 1 Phase Requirements

### 1.1 Demo Deliverable

- **Private YouTube link** 
	- Link: TBD
		- Timestamped outline:
			- 
			- 

### 1.2 Required Demo Scenarios

**Phase 2(a) - RDT 2.2 File Transfer**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |

**Phase 2(b) - Error Injection and Recovery**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |

**Phase 2(c) - Performance Evaluation**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |

### 1.3 Required Figures/Plots

Will be submitted once code is completed.

---

## 2 Phase Plan

### 2.1 Scope

**New behaviors added:** 
- Implement RDT 2.2
- Add checksum field and validation
- Add ACK packets
- Add timeouts and retransmissions at sender phase
- Add bit-error injection hooks
	- ACK corruption injection (option 2)
 	- DATA corruption injection (option 3)
- Generate plots for all 3 bit-error injection options

**Behaviors unchanged from previous phase:** 
- UDP sockets from Phase 1 used for data file transport
- File packetization still fixed into 1024 byte payloads
- Receiver reassembles file and writes to disk

**Out of scope (explicitly):**
- 

### 2.2 Acceptance Criteria 

**Phase 2(a):**
- [ ] Sender uses alternating-bit sequence numbers `(0,1)`, checksum validation, and waits for correct ACK before sending next DATA packet
- [ ] Receiver validates checksum and sequence number, delivers only the expected pacet, and responds with the appropriate ACK as per RDT 2.2 behavior

**Phase 2(b):**
- [ ] Option 1: Completes successfully with no bit errors or retransmissions
- [ ] Option 2: Detected by sender and triggers retranmission of last DATA packet
- [ ] Option 3: Detected by receiver and sends a duplicate ACK to prevent corrupted data delivery

**Phase 2(c):**
- [ ] Completion-time measurements are collected for impairment rates from 0% to 95% in 5% increments
- [ ] Each impairment rate is tested with 5 independent runs; results are averaged
- [ ] Plot is generated and included in Section 1.3

**General:**
- [ ] README.md is complete
- [ ] Invite instructor(s) to GitHub repo and include GitHub link
- [ ] Record demo and upload to YouTube 

### 2.3 Work Breakdown

**Workstream A: Cody Nguyen**
- 

**Workstream B: Olivia Pham**
- 

**Workstream C: Ian Khoo**
- 

---

## 3 Architecture and State Diagrams

### 3.1 State Diagram Evolution

#### Phase 2(a): RDT 2.2 File Transfer

```

```

#### Phase 2(b): Error Injection and Recovery

```

```

### 3.2 Component Responsibilities

**Sender Components**

`sender.py` Main Responsibilities:
- Read BMP into memory
- Compute the total number of packets using a fixed payload size 
- Divide BMP file data into chunks of 1024 bytes
- Packetize file and send via RDT 2.2
- Maintain `seq` and last sent packet
- Validate ACK checksum adn ACK number
- Implement retransmit on corrupt/wrong ACK or timeout
- Print transmission progress into console
- Phase 2(b) option 2: intentionally corrupt received ACK bits before validation

**Receiver Components**

`receiver.py` Main Responsibilities:
- Create and bind UDP socket to the specified port
- Receive DATA packets and validate checksum
- Deliver only expected `seq`
- Store payloads in a buffer indexed by sequence number
- Track the number of packets received
- Send ACK packets with checksum
- On corrupt/duplicate DATA: re-send last ACK
- Phase 2(b) option 3: intentionally corrupt received DATA bits before checksum validation
- Write the reconstructed file to disk

**Shared Modules**
- `packet.py` - Packet encoding/decoding utilities
	- Build/parse DATA and ACK packets
   	- Compute checksum

### 3.3 Message Flow Overview

#### Phase 2(a): RDT 2.2 File Transfer

```

```

#### Phase 2(b): Error Injection and Recovery

```

```

---

## 4 Packet Format

### 4.1 Packet Types
- DATA: carries file chunk with seq (0/1)
- ACK: acknowledges DATA seq (0/1)
- END: indicates end of file transfer

### 4.2 Header Fields

| Field | Size (bytes/bits) | Type | Description | Notes |
|---|---:|---|---|---|
| pkt_type | 1 | uint8 | O = DATA, 1 = ACK |  |
| seq | 1 | uint8 | DATA seq (0/1) or ACK number (0/1) | | 
| payload_length | 2 | uint16 | DATA payload size (0 for ACK) |  |
| total_packets | 4 | uint32 | Total number of DATA packets |
| checksum | 4 | uint32 | Checksum over header and payload with checksum field = 0 during calculations | | 
| payload | ≤ 1024 | bytes | File data chunk | DATA only |

**Total header size:** 12 bytes
**Maximum packet size:** 12 + 1024 = 1036 bytes

**Encoding format (Python struct):**
```python
header_format = "!BBHII"  # type, seq, payload_len, total_packets, checksum
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


