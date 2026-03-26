# Network Design Project – Phase Proposal & Design Document 
## (Phase 4 of 5)

**Team Name:**  Don't Be COI

**Members:** 
- Cody Nguyen: cody_nguyen@student.uml.edu
- Olivia Pham: olivia_pham@student.uml.edu
- Ian Khoo: ian_khoo@student.uml.edu

**GitHub Repo URL (with GitHub usernames):** https://github.com/olitranpham/network-design, olitranpham, iantkhoo1488, codynguyen-dev

**Phase:** 4

**Submission Date:**  3/21/2026

**Version:** v5

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

**Phase 4(a):** Implement the Go-Back-N (GBN) data transfer protocol over an unreliable UDP channel. Unlike the stop-and-wait model used in Phase 3 (RDT 3.0), the sender will transmit multiple packets without waiting for an ACK for each packet. A sliding window of size N will be used to allow pipelined transmission. 

**Phase 4(b):** The sender maintains a window buffer containing packets that have been sent but not yet acknowledged. If a timeout occurs, the sender will retransmit all unacknowledged packets starting from the base of the window.

**Phase 4(c):** The receiver implements the Go-Back-N receiver model, which accepts only the next expected packet in sequence and discards out-of-order packets.

**Phase 4(d):** Test the protocol under the save 5 unreliable network conditions:
	- Option 1: No loss/no bit errors
	- Option 2: ACK packet bit-error
	- Option 3: DATA packet bit-error
	- Option 4: ACK packet loss
	- Option 5: DATA packet lott

**Phase 4(e):** Evaluate protocol performance under varying loss/error probabilities and analyze the effect of window size and timeout values on completion time.

---

## 1 Phase Requirements

### 1.1 Demo Deliverable

- **Private YouTube link** 
	- Link: TBD
		- Timestamped outline:
			- TBD

### 1.2 Required Demo Scenarios

**Phase 4(a) - Go-Back-N Sliding Window Implementation**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
|   |   |   |   |
|   |   |   |   |

**Phase 4(b) - Timeout and Retransmission Logic**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
|   |   |   |   |
|   |   |   |   |

**Phase 4(c) - Go-Back-N Receiver Behavior**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
|   |   |   |   |
|   |   |   |   |

**Phase 4(d) - Error and Loss Handling**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
|   |   |   |   |
|   |   |   |   |

**Phase 4(e) - Correctness Verification**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
|   |   |   |   |
|   |   |   |   |

### 1.3 Required Figures/Plots

Plot generated and included. 

---

## 2 Phase Plan

### 2.1 Scope

**New behaviors added:** 
- Sliding window transmission
- Sender packet buffer
- Go-Back-N retransmission logic
- Cumulative acknowledgements
- Variable window size testing

**Behaviors unchanged from previous phase:** 
- UDP socket communication
- Packet checksum validation
- File segmentation into 1024-byte chunks
- Error injection mechanisms

**Out of scope (explicitly):**
- Selective repeat protocol
- Congestion control
- Adaptive timeout calculation

### 2.2 Acceptance Criteria 

**Phase 4(a):**
- [ ] The sender implements the Go-Back-N sliding window protocol over UDP.
- [ ] The sender is able to transmit multiple packets without waiting for individual ACKs.
- [ ] The sender maintains 2 variables:
      	- `base`: the sequence number of the oldest unacknowledged packet
      	- `next_seq_num`: the next packet to be transmitted
- [ ] The sender stores transmitted but unacknowledged packets in a packet buffer.
- [ ] Sequence numbers are used to identify packets and maintain correct ordering.
- [ ] The sender is able to transmit packets while `next_seq_num < base + window_size`

**Phase 4(b):**
- [ ] A single timer is maintained for the oldest unacknowledged packet.
- [ ] If the timer expires before an ACK is received, the sender retransmits all packets starting from `base` up to `next_seq_num - 1`
- [ ] The timer is restarted whenever retransmissions occur.

**Phase 4(c):**
- [ ] The receiver maintains the variable `expected_sequence_num`
- [ ] If a packet arrives with the expected sequence number, the receiver accepts the packet, the payload is delivered to the application layer, a cumulative ACK for that packet is sent, and `expected_seq_num` increments.
- [ ] If a packet arrives out of order, the packet is discarded and the receiver resends the last ACK.

**Phase 4(d):**
- [ ] Option 1: File transfer completes normally without retransmissions
- [ ] Option 2: Sender detects corrupted ACK and retransmits packets as needed
- [ ] Option 3: Receiver detects corruption and resends last ACK
- [ ] Option 4: Sender times out and retransmits packets
- [ ] Option 5: Receiver does not acknowledge missing packet, causing sender retransmission
      
**Phase 4(e):**
- [ ] Loss/error probability will range from 0% to 95% in increments of 5%.
- [ ] Each configuration will be tested five times, and results will be averaged.
- [ ] Experiments will analyze the impact of window size, timeout values, and network loss/error rates. 
      
**General:**
- [ ] README.md is complete
- [ ] Invite instructor(s) to GitHub repo and include GitHub link
- [ ] Record demo and upload to YouTube 

### 2.3 Work Breakdown

**New Tasks for Phase 4:**
- Implement Go-Back-N sliding window protocol
- Implement sender window buffer for unacknowledged packets
- Implement `base` and `next_seq_num` tracking in the sender
- Implement Go-Back-N retransmission behavior on timeout
- Modify sender logic to support pipelined packet transmission
- Modify receiver to support cumulative ACK behavior
- Test protocol under unreliable channel scenarios (Options 1–5)
- Evaluate protocol performance under different window sizes and loss/error probabilities

**Workstream A: Cody Nguyen**
- Integrate Go-Back-N logic into the existing UDP file transfer framework.
- Implement and validate error injection scenarios (Options 1–5).
- Ensure sender correctly handles corrupted or lost ACK packets.
- Verify retransmission behavior under packet loss conditions.

**Workstream B: Olivia Pham**
- Design and implement the Go-Back-N sender architecture.
- Implement sliding window transmission logic (`base`, `next_seq_num`, window size).
- Implement packet buffering for unacknowledged packets.
- Implement timeout and retransmission of packets starting from the window base.
  
**Workstream C: Ian Khoo**
- Conduct performance evaluation experiments across varying loss/error probabilities.
- Test protocol behavior with different window sizes.
- Measure completion times for file transfers under all scenarios.
- Generate performance plots and record demonstration videos for Phase 4.

---

## 3 Architecture and State Diagrams

### 3.1 State Diagram Evolution

#### Phase 4(a): Go-Back-N Sliding Window Implementation

```


```

#### Phase 4(b): Timeout and Retransmission Logic

```

```

#### Phase 4(c): Go-Back-N Receiver Behavior

```

```

#### Phase 4(d): Error and Loss Handling

```

```

### 3.2 Component Responsibilities

**Phase 3(a) - Sender Components**

`sender.py` Main Responsibilities:
- Read BMP into memory
- Compute the total number of packets using a fixed payload size 
- Divide BMP file data into chunks of 1024 bytes
- Packetize file and send via RDT 3.0
- Maintain `seq` and last sent packet
- Validate ACK checksum adn ACK number
- Implement retransmit on corrupt/wrong ACK or timeout
- Print transmission progress into console
- Phase 3 option 2: intentionally corrupt received ACK bits before validation
- Phase 3 option 4: intentionally lose received ACK bits before validation

**Phase 3(a) - Receiver Components**

`receiver.py` Main Responsibilities:
- Create and bind UDP socket to the specified port
- Receive DATA packets and validate checksum
- Deliver only expected `seq`
- Store payloads in a buffer indexed by sequence number
- Track the number of packets received
- Send ACK packets with checksum
- On corrupt/duplicate DATA: re-send last ACK
- Phase 3 option 3: intentionally corrupt received DATA bits before checksum validation
- Phase 3 option 5: intentionally lose received DATA bits before checksum validation
- Write the reconstructed file to disk


**Shared Modules**
- `packet.py` - Packet encoding/decoding utilities
	- Build/parse DATA and ACK packets
   	- Compute checksum

### 3.3 Message Flow Overview

#### Phase 3(a): RDT 3.0 File Transfer CHANGE THIS FOR PHASE3

```
    SENDER                                              RECEIVER
    ======                                              ========
    
    seq = 0                                             expected_seq = 0
    |                                                   |
    | Create pkt0                                       |
    | Checksum: 0xAB12                                  |
    | Start timer                                       |
    |------------- DATA(seq=0, "chunk0") -------------->|
    |              [Type='D', Seq=0, Len=1024]          |
    |              [Payload=chunk0, Checksum=0xAB12]    |
    |                                                   | Validate checksum 
    |                                                   | expected_seq == 0 
    | retransmit pkt if timer runs out                  | Deliver chunk0 to buffer[0]
    |                                                   | expected_seq = 1
    |                                                   |
    |<------------- ACK(ack_num=0) ---------------------|
    |              [Type='A', ACK=0, Checksum=0x1234]   |
    | Validate checksum                                 |
    | ACK matches seq                                   |
    | seq = 1                                           |
    |                                                   |
    |                                                   |
    | Create pkt1                                       |
    | Checksum: 0xCD34                                  |
    |                                                   |
    |------------- DATA(seq=1, "chunk1") -------------->|
    |              [Type='D', Seq=1, Len=1024]          |
    |              [Payload=chunk1, Checksum=0xCD34]    |
    |                                                   | Validate checksum 
    |                                                   | expected_seq == 1 
    |                                                   | Deliver chunk1 to buffer[1]
    |                                                   | expected_seq = 0
    |                                                   |
    |<------------- ACK(ack_num=1) ---------------------|
    |              [Type='A', ACK=1, Checksum=0x5678]   |
    | Validate checksum                                 |
    | ACK matches seq                                   |
    | seq = 0                                           |
    | -------------- Continue until all data sent ----- |
    | Transfer complete                                 | File reconstruction complete
    | n packets sent                                    | n packets received
    | x retransmission(s)                               | Write output.bmp

```

#### Phase 3(b): Error Injection and Recovery

```
Option 1 No Error / Data Loss is the same diagram as Phase 2(a)

Option 2 Corrupt ACK Packet OR Loss ACK Packet w/ example data: 
    SENDER                                              RECEIVER
    ======                                              ========
    
    seq = 0                                             expected_seq = 0
    |                                                   |
    | Create pkt0                                       |
    | Start timer                                       |
    |------------- DATA(seq=0, "chunk0") -------------->|
    |              Checksum=0xAB12                      |
    | ┌─────────────────────────────────────────┐       |
    | │ ERROR INJECTION (Option 4)              │       |
    | │ Lost ACK before validation              │       |
    | │ ACK corrupted: 0x5678 → nothing         │       |
    | └─────────────────────────────────────────┘       |
    |                                                   | Validate checksum 
    |                                                   | Deliver chunk0
    |                                                   | expected_seq = 1
    |                                                   |
    |                                                   |
    |        X----- ACK LOST----------------------------|
    |              Checksum=0x1234                      |
    | Timer ends - No ACK received, retransmit          |
    | Retransmit packet 0                               |
    |------------- DATA(seq=0, "chunk0") -------------->|
    |              Checksum=0xAB12                      |
    |                                                   | Validate checksum 
    |                                                   | Deliver chunk0
    |                                                   | expected_seq = 1
    |                                                   |
    |                                                   |
    | Validate checksum                                 |
    | seq = 1                                           |
    |                                                   |
    |<------------- ACK(ack_num=0) ---------------------|
    |              Checksum=0x1234                      |
    | Validate checksum                                 |
    | seq = 1                                           |
    |                                                   |
    |                                                   |
    | Create pkt1                                       |
    |                                                   |
    |------------- DATA(seq=1, "chunk1") -------------->|
    |              Checksum=0xCD34                      |
    |                                                   | Validate checksum 
    |                                                   | Deliver chunk1
    |                                                   | expected_seq = 0
    |                                                   |
    |<------------- ACK(ack_num=1) ---------------------|
    |              Checksum=0x5678                      |
    |                                                   |
    | ┌─────────────────────────────────────────┐       |
    | │ ERROR INJECTION (Option 2)              │       |
    | │ Flip bits in ACK before validation      │       |
    | │ ACK corrupted: 0x5678 → 0x56FF          │       |
    | └─────────────────────────────────────────┘       |
    |                                                   |
    | Validate checksum: FAIL                           |
    | Check ACK: Corrupt ACK detected                   |
    | Retransmit packet 1                               |
    |                                                   |
    |                                                   |
    |------------- DATA(seq=1, "chunk1") -------------->|
    |              [RETRANSMISSION]                     |
    |              Checksum=0xCD34                      |
    |                                                   | Validate checksum 
    |                                                   | seq == expected_seq? if no, dupe
    |                                                   | Already have chunk1
    |                                                   | Resend ACK1
    |                                                   |
    |<------------- ACK(ack_num=1) ---------------------|
    |              Checksum=0x5678                      |
    | Validate checksum                                 |
    | ACK matches seq                                   |
    | seq = 0                                           |
    |                                                   |
    | -------------- Continue until all data sent ----- |
    | Transfer complete                                 | File reconstruction complete
    | n packets sent                                    | n packets received
    | x retransmission(s)                               |

Option 3/5 Data bit-Error OR Loss data w/ example data:
    SENDER                                              RECEIVER
    ======                                              ========
    
    seq = 0                                             expected_seq = 0
    |                                                   |
    | Create pkt0                                       |
    | Start timer                                       |
    |                                                   |
    |------------- DATA(seq=0, "chunk0") --------X      |
    |              Checksum=0xAB12                      |
    |                                                   | ┌────────────────────────────┐
    |                                                   | │ ERROR INJECTION (Option 5) │
    |                                                   | │ Lost DATA before checksum  │
    |                                                   | │ 0xCD34 → Nothing           │
    |                                                   | └────────────────────────────┘
    |                                                   |
    |                                                   | Validate checksum: FAIL
    |                                                   | Corrupt DATA detected
    |                                                   | Send last valid ACK (ACK0)
    |                                                   | Do NOT deliver data
    |                                                   | Do NOT change expected_seq
    | Timer ends - No ACK received, retransmit          |
    | Retransmit packet 0                               |
    |------------- DATA(seq=0, "chunk0") -------------->|
    |              Checksum=0xAB12                      |
    |                                                   |
    |                                                   |
    |                                                   | Validate checksum 
    |                                                   | Deliver chunk0
    |                                                   | expected_seq = 1
    |                                                   | last_ack = 0
    |                                                   |
    |<------------- ACK(ack_num=0) ---------------------|
    | Validate checksum                                 |
    | seq = 1                                           |
    |                                                   |
    |                                                   |
    | Create pkt1                                       |
    |                                                   |
    |------------- DATA(seq=1, "chunk1") -------------->|
    |              Checksum=0xCD34                      |
    |                                                   |
    |                                                   | ┌────────────────────────────┐
    |                                                   | │ ERROR INJECTION (Option 3) │
    |                                                   | │ Flip bits before checksum  │
    |                                                   | │ 0xCD34 → 0xCDFF            │
    |                                                   | └────────────────────────────┘
    |                                                   |
    |                                                   | Validate checksum: FAIL
    |                                                   | Corrupt DATA detected
    |                                                   | Send last valid ACK (ACK0)
    |                                                   | Do NOT deliver data
    |                                                   | Do NOT change expected_seq
    |                                                   |
    |<------------- ACK(ack_num=0) ---------------------|
    |              [Last valid ACK]                     |
    | Validate checksum                                 |
    | Check ACK (Expected ACK1, got ACK0)               |
    | Retransmit packet 1                               |
    |                                                   |
    |                                                   |
    |------------- DATA(seq=1, "chunk1") -------------->|
    |              [RETRANSMISSION]                     |
    |              Checksum=0xCD34                      |
    |                                                   | Validate checksum 
    |                                                   | expected_seq == 1 
    |                                                   | Deliver chunk1
    |                                                   | expected_seq = 0
    |                                                   | last_ack = 1
    |                                                   |
    |<------------- ACK(ack_num=1) ---------------------|
    | Validate checksum                                 |
    | ACK matches seq                                   |
    | seq = 0                                           |
    | -------------- Continue until all data sent ----- |
    | Transfer complete!                                | File reconstruction complete!
    | n packets sent                                    | n unique packets received
    | x retransmission(s)                               |

```

---

## 4 Packet Format

### 4.1 Packet Types
- DATA: carries file chunk with seq (0/1)
- ACK: acknowledges DATA seq (0/1)

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

**RDT 3.0 Packet Structure** (in `packet.py`)

- Fields:
  - `pkt_type` (uint8): Packet type identifier (DATA/ACK)
  - `seq` (uint8): Sequence number (alternating bit: 0/1)
  - `payload_length`(uint32): Number of valid bytes in the payload (0 for ACK packets)
  - `total_packets` (uint32): Total number of DATA packets in the transfer
  - `checksum` (uint32): Checksum computer over header and payload
  - `payload` (bytes): File data chunk (up to 1024 bytes)

- Invariants:
  - `seq ∈ {0, 1}`
  - `0 <= payload_length <= 1024`
  - `total_packets >= 1`

**Sender Transmission State** (in `sender.py`)

- Fields:
  - `seq` (uint8): Current sequence number
  - `last_packet` (bytes): Most recently transmitted DATA packet
  - `file_data` (int): Size of the input file in bytes
  - `total_packets` (int): Total number of DATA packets to send
  - `timeout` (float): Sender timeout duration in seconds

- Invariants:
  - `file_size == len(file_data)`
  - `total_packets == (file_size + MAX_PAYLOAD - 1) // MAX_PAYLOAD`
  - `last_packet` is retransmitted upon timeout or corrupt/invalid ACK
  - Sender transmits one DATA packet at a time
  - Sender advances `seq` only after receiving a valid ACK

**Receiver Reception State** (in `receiver.py`)

- Fields:
  - `expected_seq` (uint8): Sequence number expected
  - `last_ack` (bytes): Most recently sent valid ACK packet
  - `packets` (list): List of packet payloads indexed by `seq`
  - `total_packets` (int): Expected total number of packets (from first received packet)
  - `received_count` (int): Number of packets successfully received

- Invariants:
  - Receiver delivers DATA only if packet is valid/non-corrupt and `seq == expected_seq`
  - Dupllicate or corrupt DATA packets are not delivered
  - `received_count <= total_packets`
  - Transfer completed when `received_count == total_packets`
  - Receiver always responds to invalid or duplicate DATA with `last_ack`

### 5.2 Module Map and Dependencies

```
src/
|-- sender.py       	# Phase 3(a): RDT 3.0 file sender
|-- receiver.py   	 	# Phase 3(a): RDT 3.0 file receiver
|-- packet.py  			# Phase 3(a): DATA/ACK packet creation, parsing, and checksum utilities
|-- channel.py			# Phase 3(b): Bit-error injection and unreliable channel simulation 
|-- experiments.py		# Phase 3(c): Completion-time experiments and data collection
```

**Dependency Graph:**

```
sender.py       -> socket, argparse, packet.py, channel.py, time
receiver.py     -> socket, argparse, packet.py, channel.py

packet.py       -> struct, zlib (or checksum utility)
channel.py      -> random

experiments.py  -> subprocess, time, csv, matplotlib
```

## 6 Protocol Logic 

### 6.1 Sender Behavior

**Phase 3(a) - RDT 3.0 File Transfer**

Steps:
1. Open BMP file
2. Read the file and split into fixed-size chunks (<= 1024 bytes)
3. Initialize alternating-bit sequence number
4. For each chunk:
	a. Create DATA packet containing the sequence number, payload length, total packet count, checksum, and payload
	b. Send the DATA packet over UDP socket
	c. Start a timer and wait for an ACK
5. Upon receiving ACK
   	a. Validate checksum and sequence number
   	b. If the ACK is valid and matches the current sequence number, stop the timer and toggle the sequence number
6. Continue until all file chunks are transmitted 

**Phase 3(a) Sender Pseudocode:**

```
initialize seq = 0
read input file and compute total_packets

for each chunk in file do
	packet <- make_DATA_packet(seq, chunk, total_packets)
	send packet over UDP
	start timer

	wait for ACK or timeout
	if ACK received and valid AND ACK.seq == seq then
		stop timer
		seq <- toggle(seq0
	else
		retransmit packet
	end if
end for
```

**Phase 3(Option 2/4) - Error Injection and Recovery**

Steps:
1. Enable error injection based on option 1, 2, 3, 4, or 5 (ACK/DATA corruption)
2. After sending a DATA packet, wait for an ACK
3. If the ACK is corrupted, invalid, or times out:
	a. Retransmit the previously sent DATA packet
4. Continue retransmission until a valid ACK is received
5. Only advance the sequence number after successful ACK validation
	
**Phase 3(b) Pseudocode:**

```
initialize seq = 0
initialize last_packet = null

for each chunk in file do
    last_packet <- make_DATA_packet(seq, chunk, total_packets)
    send last_packet over UDP
    start timer

    while true do
        wait for ACK or timeout
        if timeout OR ACK corrupt OR ACK.seq != seq then
            retransmit last_packet
            restart timer
        else
            stop timer
            seq <- toggle(seq)
            break
        end if
    end while
end for
```

### 6.2 Receiver Behavior

**Phase 3(a) - RDT 3.0 File Transfer**
Steps:
1. Bind UDP socket to the receiver port
2. Initialize the expected sequence number
3. Initialize a buffer for storing received payloads
4. Initialize a timer for packet loss scenarios
5. Loop until all packets are received:
	a. Receive a DATA packet
	b. Validate the checksum and sequence number
	c. If the packet is valid and matches the expected sequence number:
		i. Deliver the payload and store it
		ii. Send an ACK for the received sequence number
		iii. Toggle the expected sequence number
	d. Otherwise, resend the last valid ACK

**Phase 3(b) Receiver Pseudocode:**

```
initialize expected_seq = 0
initialize last_ack = ACK(1)
initialize received_count = 0

while received_count < total_packets do
    Receive a packet from UDP

    if packet corrupt OR packet.seq != expected_seq then
        send last_ack
    else
        deliver payload
        store payload
        last_ack <- make_ACK(expected_seq)
        send last_ack
        expected_seq <- toggle(expected_seq)
        received_count <- received_count + 1
    end if
end while

reassemble file and write to disk
close socket
```

**Phase 3(Option 3/5) - Error Injection and Recovery** 
Steps:
1. Enable DATA bit-error or loss injection if configured
2. Once receiving corrupted DATA packet:
	a. Discard the packet
	b. Send the last valid ACK
3. Once receiving a duplicate DATA packet:
	a. Do not deliver the payload
	b. Send the last valid ACK
4. Once receiving the DATA packet, set to be lost:
	a. Do not deliver the payload
	b. Do not send ACK 
6. Continue as normal once a valid packet is received

**Phase 3(b) Receiver Pseudocode:**

```
if received DATA packet is corrupt then
    discard packet
    send last_ack
else if packet.seq != expected_seq then
    discard packet
    send last_ack
else
    accept packet
    deliver payload
    send ACK(expected_seq)
    expected_seq ← toggle(expected_seq)
end if
```

### 6.3 Error / Loss Injection Specification
During Phase 3(b):
ACK packet Bit error - ACK packet will be intentionally changed at the sender 
	-ACK will be changed randomly.
Data packet bit error - Data packet will be intentionally changed at the receiver
	-Bits will be flipped randomly 
ACK packet Loss error - ACK packet will intentionally be lost at the sender
	-ACK will not be sent/received
Data packet Loss error - data packet will intentionally be lost at the receiver
	-Data will not be sent/received

---

## 7 Experiments and Metrics Plan

Phase 3 evaluates the performance and correctness of RDT 3.0 under unreliable channel conditions

The same BMP file is transferred under three scenarios
- Option 1: No bit-errors: Baseline performance
- Option 2: ACK packet bit-error injection: Bit errors are intentionally introduced into ACK packets at the sender’s receive path
- Option 3: DATA packet bit-error injection: Bit errors are intentionally introduced into DATA packets at the receiver’s receive path
- Option 4: ACK packet loss: ACK packets are intentionally dropped at the sender receive path
- Option 5: DATA packet loss: DATA packets are intentionally dropped at the receiver

### 7.1 Setup
- Payload size: 1024 bytes
- Non-pipelined stop-and-wait behavior
- Sequence numbers: alternating bit (0/1)
- Checksum: CRC32
- Loss/error rates: Transfers are executed across error rates from 0% to 95% in increments of 5%

Each rate is tested:
- 5 independent runs
- Same input BMP file
- Debug logging disabled during timing

### 7.2 Timing Measurement 
End-to-end completion time is measured at the sender and includes:
- Retransmissions
- ACK recovery
- All protocol overhead
It ends when the final packet is acknowledged.

### 7.3 Plot Generation 
A single plot is generated with:
- X-axis: error rate (%)
- Y-axis: average completion time (seconds)
- Five lines representing Options 1, 2, 3, 4, and 5
- Completion time is expected to increase as error rate rises

### 7.4 Correctness Validation
For every run:
- The output file must match the input file byte-for-byte.
- Sequence numbers must alternate correctly.
- No deadlocks or infinite retransmissions may occur.


**Output Artifacts:**
- `results/phase3_raw.csv` (timing + status per attempt)
- `results/phase3_avg.csv` (average completion time per rate per option)
- `results/phase3_plot.gp` (gnuplot script)
- `results/phase3_plot.png` (plot image, if gnuplot is installed)

---

## 8 Edge Cases and Test Plan
Phase 3 must validate RDT 3.0

### 8.1 Expected Edge Cases

| Edge case | Why it matters | Expected behavior |
|---|---|---|
| last packet smaller than payload size | correct file reconstruction | receiver writes exact bytes |
| Corrupted DATA/ACK packet | Receiver must detect via checksum | Receiver discards packet and resends last DATA/ACK packet |
| Duplicate DATA/ACK packet | Caused by lost ACK or retransmission | Receiver resends ACK but does not deliver duplicate, or sender ignores if incorrect seq|
| High error rate (≥80%) | Stress test | Transfer completes eventually |
| Wrong seq ACK | Protocol correctness | sender ignores ACK and retransmits last DATA packet after timeout |
| Lost DATA packet | No ACK received | sender times out and retransmits |
| Lost ACK packet | Sender never sees ACK | sender times out and retransmits |

### 8.2 Tests
- `test_make_parse_roundtrip`: `make_packet(seq, payload, total)` then `parse_packet()` returns the same fields
- `test_max_payload_1024`: payload of exactly 1024 bytes encodes/decodes correctly
- `test_small_payload`: payloads of less than 1024 bytes encodes/decodes correctly
- `test_checksum_correct`: checksum function produces the expected value and detects corruption
- `test_ack_packet_format`: ACK packets are encoded/decoded correctly and contain only ACK fields.
- `test_data_packet_format`: DATA packets include expected fields and validate correctly.

**Integration Tests:**
Option 1: 
- Transfer file
- Confirm byte match
Option 2:
- Corrupt ACK with probability p
- Confirm retransmission logic works
- Confirm file correctness
Option 3:
- Corrupt DATA with probability p
- Confirm receiver discards corrupted packet
- Confirm retransmission occurs
Option 4:
- Lose ACK with probability p
- Confirm retransmission logic works
- Confirm file correctness
Option 5:
- Lose DATA with probability p
- Confirm receiver discards corrupted packet
- Confirm retransmission occurs

### 8.3 Test Artifacts

- Console logs saved to `results/logs/`
- Output files from tests in `results/`
- Test scripts in `tests/`

### 8.4 FSM Validation
Ensure sender states match textbook FSM 

Sender states:
- Wait for call from above
- Wait for ACK 0
- Wait for call 1 from above
- Wait for ACK 1

Receiver states:
- Wait for 0
- Wait for 1

Each transition must match the RDT 2.2 diagram.
---

## 9 Repository Structure and Reproducibility
```
src/
  sender.py
  receiver.py
  packet.py
  channel.py

scripts/
  phase3_experiments.py

results/
 phase3_raw.csv  
 phase3_avg.csv  
 phase3_plot.gp  
 phase3_plot.png  

test-files/
  sample1.bmp
```

**To reproduce:**
Refer to README

---

## 10 Team Plan, Ownership, and Milestones

### 10.1 Task Ownership

| Task | Owner | Target Date | Definition of Done |
|---|---|---|---|
| Implement RDT 3.0 sender loop | Olivia Pham | 3/17/26 | Sender transmits DATA packets with alternating-bit seq, waits for ACK before advancing, and supports configurable timeout. |
| Implement ACK validation + retransmission logic | Olivia Pham | 3/17/26 | Sender correctly detects corrupt/wrong-seq ACKs and retransmits the last DATA packet until a valid ACK is received. |
| Implement RDT 3.0 receiver accept/duplicate/corrupt handling | Olivia Pham | 3/17/26 | Receiver validates checksum, delivers only expected seq packets, discards corrupt/duplicate packets, and responds with correct ACK or last ACK. |
| Implement ACK bit-error injection | Cody Nguyen | 2/20/26 | ACK corruption is applied; sender detects corruption and retransmits; transfer still completes with correct output file. |
| Implement DATA bit-error injection | Cody Nguyen | 2/20/26 | DATA corruption is applied, receiver discards corrupted packets, re-sends last ACK, and file transfer completes correctly. |
| Implement end-to-end correctness | Cody Nguyen | 2/20/26 | verifies received BMP matches the original for Options 1–3 across multiple runs. |
| Test and ensure all files and scripts can be run, debug, and changed if needed | Ian Khoo | 3/18/26 | tests are run and scripts are updated |
| Collect completion time measurements in 5% increments | Ian Khoo | 3/19/26 | Measurements are collected |
| Generate plot of collected data | Ian Khoo | 3/19/26 | Plot is generated and sharable |
| Implement ACK packet loss | Cody Nguyen | 3/18/26 | ACK loss is injected and sender retransmits correctly |
| Implement DATA packet loss | Cody Nguyen | 3/18/26 | DATA loss is injected and sender retransmits correctly |

### 10.2 Milestones

1.  ACK is successfully implemented into the sender/receiver logic
2.  Receiver/Sender is able to detect and validate errors
3.  ACK packet bit error is correctly changing the data of the ACK
4.  The data packet bit error is correctly changing the data of the data packet
5.  ACK packet loss error is correctly losing the data of the ACK
6.  The data packet loss error is correctly changing, losing the data of the data packet
7.  Completion time measurements are collected, and each impairment rate is tested with 5 independent runs, with results averaged.
8.  Plot with all data from completion time is generated
9.  Videos of working code are taken.

---

## 11 Demonstration Checklist

### Pre-Recording Checklist

**Phase 3(Option 1):**
- [X] Both terminal windows visible side-by-side

**Phase 3(Option 2):**
- [X] Both terminal windows visible side-by-side
- [X] Terminal that shows error injection open

**Phase 3(Option 3):**
- [X] Both terminal windows visible side-by-side
- [X] Terminal that shows error injection open

**Phase 3(Option 4):**
- [X] Both terminal windows visible side-by-side
- [X] Terminal that shows error injection open

**Phase 3(Option 5):**
- [X] Both terminal windows visible side-by-side
- [X] Terminal that shows error injection open
      
**Video Quality:**
- [X] Both terminal windows visible side-by-side
- [X] Clear explanation of steps
- [X] Show file comparison/verification


