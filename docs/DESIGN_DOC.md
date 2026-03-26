# Network Design Project – Phase Proposal & Design Document 
## (Phase 4 of 5)

**Team Name:**  Don't Be COI

**Members:** 
- Cody Nguyen: cody_nguyen@student.uml.edu
- Olivia Pham: olivia_pham@student.uml.edu
- Ian Khoo: ian_khoo@student.uml.edu

**GitHub Repo URL (with GitHub usernames):** https://github.com/olitranpham/network-design, olitranpham, iantkhoo1488, codynguyen-dev

**Phase:** 4

**Submission Date:**  3/31/2026

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
	- Option 5: DATA packet loss

**Phase 4(e):** Evaluate protocol performance under varying loss/error probabilities and analyze the effect of window size and timeout values on completion time.

---

## 1 Phase Requirements

### 1.1 Demo Deliverable

- **Private YouTube link** 
	- Link: TBD
		- Timestamped outline:
			- TBD

### 1.2 Required Demo Scenarios

**Phase 4(a) - Go-Back-N File Transfer**

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

#### Phase 4(a): Go-Back-N File Transfer

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

**Phase 4(a-b) - Sender Components**

`sender.py` Main Responsibilities:
- Read BMP into memory
- Compute the total number of packets using a fixed payload size 
- Divide BMP file data into chunks of 1024 bytes
- Packetize file and transmit using the Go-Back-N protocol
- Maintain sliding window variables
	- `base`: sequence number of the oldest unacknowledged packet
   	- `next_seq_num`: next packet sequence number to send
- Maintain a window buffer containing packets that have been sent but not yet acknowledged
- Send packets while `next_seq_num < base + window_size`
- Start a timer for the oldest unacknowledged packet
- Process cumulative ACK packets received from the receiver
- Update `base` when valid ACKs are received
- Print transmission progress into console
- Phase 4 option 2: intentionally corrupt received ACK bits before validation
- Phase 4 option 4: intentionally drop received ACK packets before validation

**Phase 4(c) - Receiver Components**

`receiver.py` Main Responsibilities:
- Create and bind UDP socket to the specified port
- Receive DATA packets and validate checksum
- Maintain `expected_seq_num` for Go-Back-N reception
- Accept and deliver packets only if `seq == expected_seq_num`
- Deliver payload data to the application layer in order
- Send cumulative ACK packets for the last correctly received packet
- Discard out-of-order packets
- For corrupt/unexpected DATA packets -> resend last valid ACK
- Phase 4 option 3: intentionally corrupt received DATA bits before checksum validation
- Phase 4 option 5: intentionally drop received DATA packets before processing
- Write the reconstructed file to disk

**Shared Modules**
- `packet.py` - Packet encoding/decoding utilities
	- Build and parse DATA packets
	- Build and parse ACK packets
	- Compute packet checksum for error detection
	- Provide packet structure utilities used by both sender and receiver

### 3.3 Message Flow Overview

#### Phase 4(a): Go-Back-N File Transfer

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
---

## 4 Packet Format

### 4.1 Packet Types
- DATA: carries file chunk with a sequence number
- ACK: cumulative acknowledgment indicating the highest in-order packet received

### 4.2 Header Fields

| Field | Size (bytes/bits) | Type | Description | Notes |
|---|---:|---|---|---|
| pkt_type | 1 | uint8 | O = DATA, 1 = ACK | Identifies packet type |
| seq | 4 | uint32 | DATA seq (0/1) or ACK number (0/1) | Used for Go-Back-N sliding window | 
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

**Go-Back-N Packet Structure** (in `packet.py`)

- Fields:
  - `pkt_type` (uint8): Packet type identifier (DATA/ACK)
  - `seq` (uint32): Sequence number used for Go-Back-N transmission
  - `payload_length`(uint16): Number of valid bytes in the payload (0 for ACK packets)
  - `total_packets` (uint32): Total number of DATA packets in the transfer
  - `checksum` (uint32): Checksum computer over header and payload
  - `payload` (bytes): File data chunk (up to 1024 bytes)

- Invariants:
  - `0 <= payload_length <= 1024`
  - `total_packets >= 1`

**Sender Transmission State** (in `sender.py`)

- Fields:
  - `base` (uint32): Sequence number of the oldest unacknowledged packet
  - `next_seq_num` (uint32): Sequence number of the next packet to send
  - `window_size` (int): Maximum number of packets allowed in the sender window
  - `packet_buffer` (list): Buffer storing transmitted but unacknowledged packets
  - `file_data` (bytes): Contents of the input file
  - `total_packets` (int): Total number of DATA packets to send
  - `timeout` (float): Sender timeout duration in seconds

- Invariants:
  - `base <= next_seq_num`
  - Sender transmits packets while `next_seq_num < base + window_size`
  - If timeout occurs, sender retransmits packets fro `base` to `next_seq_num - 1`

**Receiver Reception State** (in `receiver.py`)

- Fields:
  - `expected_seq` (uint32): Sequence number expected
  - `last_ack` (bytes): Most recently sent valid ACK packet
  - `received_packets` (list): Storage for received payload data
  - `total_packets` (int): Expected total number of packets (from first received packet)
  - `received_count` (int): Number of packets successfully received

- Invariants:
  - Receiver delivers DATA only if packet is valid/non-corrupt and `seq == expected_seq`
  - Duplicate or corrupt DATA packets are not delivered
  - Transfer completed when `received_count == total_packets`
  - Receiver sends cumulative ACKs for the last correctly received packet

### 5.2 Module Map and Dependencies

```
src/
|-- sender.py          # Phase 4(a): Go-Back-N sender
|-- receiver.py        # Phase 4(c): Go-Back-N receiver
|-- packet.py          # Packet creation, parsing, and checksum utilities
|-- channel.py         # Bit-error and packet loss injection simulation
|-- experiments.py     # Completion-time experiments and data collection
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

**Phase 4(a) - Go-Back-N File Transfer**

Steps:
1. Open BMP file
2. Read the file and split into fixed-size chunks (<= 1024 bytes)
3. Initialize sender variables:
	a. `base = 0`
	b. `next_seq_num = 0`
	c. `window_size = N`
4. While packets remain to be sent:
	a. If `next_seq_num < base + window_size`, create and send DATA packet
	b. If `base == next_seq_num`, start timer
	c. Increment `next_seq_num`
5. Upon receiving ACK
   	a. Validate checksum
   	b. Update `base = ack_num + 1`
   	c. If `base == next_seq_num`, stop timer
   	d. Otherwise, start timer
   	b. If the ACK is valid and matches the current sequence number, stop the timer and toggle the sequence number
6. If timeout occurs, retransmit all packets from `base` to `next_seq_num - 1`
7. Continue until all packets are acknowledged

**Phase 4(b) Sender Pseudocode:**

```
initialize base = 0
initialize next_seq_num = 0

while base < total_packets do

    if next_seq_num < base + window_size then
        send packet[next_seq_num]

        if base == next_seq_num then
            start timer
        end if

        next_seq_num += 1
    end if

    if ACK received then
        base = ACK + 1

        if base == next_seq_num then
            stop timer
        else
            restart timer
        end if
    end if

    if timeout then
        for i from base to next_seq_num - 1 do
            retransmit packet[i]
        end for
        restart timer
    end if

end while
```

### 6.2 Receiver Behavior

**Phase 4(c) - Go-Back-N Receiver**

Steps:
1. Bind UDP socket to receiver port
2. Initialize `expected_seq = 0`
3. Loop unntil all packets are received (receive DATA packet and validate checksum)
4. If packet is valid and `seq == expected_seq`:
	a. Deliver payload
	b. Store payload
	c. Send ACK
	d. Increment `expected_seq`
7. If the ACK is corrupted, invalid, or times out:
	a. Discard packet
	b. Send last valid ACK
9. Continue retransmission until a valid ACK is received
	
**Phase 4(c) Pseudocode:**

```
initialize expected_seq = 0
initialize last_ack = ACK(-1)

while received_count < total_packets do

    receive packet

    if packet corrupt OR packet.seq != expected_seq then
        send last_ack

    else
        deliver payload
        store payload
        last_ack = make_ACK(expected_seq)
        send last_ack
        expected_seq += 1
        received_count += 1
    end if

end while

reassemble file and write to disk
```

### 6.3 Error / Loss Injection Specification

During Phase 4(d) testing:
- ACK packet bit error: ACK packet will be intentionally changed at the sender
- DATA packet bit error: Data packet will be intentionally changed at the receiver
- ACK packet loss error: ACK packet will intentionally be lost at the sender
- DATA packet loss error: DATA packet will intentionally be lost at the receiver

---

## 7 Experiments and Metrics Plan

Phase 4 evaluates Go-Back-N performance under unreliable channel conditions.

The same BMP file is transferred under 5 scenarios: 
- Option 1: No bit errors
- Option 2: ACK packet bit-error
- Option 3: DATA packet bit-error
- Option 4: ACK packet loss
- Option 5: DATA packet loss

### 7.1 Setup
- Payload size: 1024 bytes
- Sliding window transmission (Go-Back-N)
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
- Sliding-window pipeline overhead
Timing ends when the final packet is acknowledged.

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
- TBD

---

## 8 Edge Cases and Test Plan

Phase 4 must validate the Go-Back-N protocol implementation.

### 8.1 Expected Edge Cases

| Edge case | Why it matters | Expected behavior |
|---|---|---|
| Last packet smaller than payload size | Correct file reconstruction | Receiver writes exact bytes |
| Corrupted DATA packet | Receiver must detect via checksum | Receiver discards packet and sends last valid ACK |
| Corrupted ACK packet | Sender must detect corruption | Sender ignores ACK and retransmits after timeout |
| Duplicate DATA packet | Caused by retransmission | Receiver discards packet and resends last ACK |
| Out of order packet | Occurs with Go-Back-N pipeline | Receiver discards packet and sends last ACK | 
| High error rate (≥80%) | Stress test | Transfer completes eventually |
| Lost DATA packet | Receiver never receives packet | Sender times out and retransmits |
| Lost ACK packet | Sender never sees ACK | Sender times out and retransmits |

### 8.2 Tests
- `test_make_parse_roundtrip`: `make_packet(seq, payload, total)` then `parse_packet()` returns the same fields
- `test_max_payload_1024`: payload of exactly 1024 bytes encodes/decodes correctly
- `test_small_payload`: payloads of less than 1024 bytes encodes/decodes correctly
- `test_checksum_correct`: checksum function produces the expected value and detects corruption
- `test_ack_packet_format`: ACK packets are encoded/decoded correctly and contain only ACK fields.
- `test_data_packet_format`: DATA packets include expected fields and validate correctly.

**Integration Tests:**
Option 1 - No loss: 
- Transfer file
- Confirm byte match
  
Option 2 - ACK corruption: 
- Corrupt ACK packets with probability p
- Sender detects corruption
- Sender retransmits window
  
Option 3 - DATA corruption:
- Corrupt DATA with probability p
- Confirm receiver discards corrupted packet
- Confirm retransmission occurs
  
Option 4 - ACK loss:
- Lose ACK with probability p
- Confirm retransmission logic works
- Confirm file correctness
  
Option 5 - DATA loss:
- Lose DATA with probability p
- Confirm receiver discards corrupted packet
- Confirm retransmission occurs

### 8.3 Test Artifacts

- Console logs saved to `results/logs/`
- Output files from tests in `results/`
- Test scripts in `tests/`

### 8.4 FSM Validation

Ensure sender states match Go-Back-N FSM behavior.

Sender states:
- Send packets within sliding window
- Wait for ACKs
- Retransmit packets on timeout

Receiver states:
- Wait for expected packet
- Accept in-order packet
- Send cumulative ACK
- Discard out-of-order packets

---

## 9 Repository Structure and Reproducibility
```
src/
  sender.py
  receiver.py
  packet.py
  channel.py

scripts/
  phase4_experiments.py

results/
  phase4_raw.csv
  phase4_avg.csv
  phase4_plot.gp
  phase4_plot.png

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
| Implement Go-Back-N sender sliding window | Olivia Pham | 4/8/26 | Sender supports `base`, `next_seq_num`, and configurable window size |
| Implement packet buffering and retransmission | Olivia Pham | 4/8/26 | Sender retransmits packets from base on timeout |
| Implement Go-Back-N receiver logic | Olivia Pham | 4/8/266 | Receiver accepts only expected packets and sends cumulative ACKs |
| Implement ACK bit-error injection | Cody Nguyen | 4/8/26 | ACK corruption is applied and handled correctly |
| Implement DATA bit-error injection | Cody Nguyen | 4/8/26 | DATA corruption detected and handled |
| Implement ACK packet loss | Cody Nguyen | 4/8/26 | ACK loss causes timeout and retransmission |
| Implement DATA packet loss | Cody Nguyen | 4/8/26 | DATA loss triggers retransmission |
| Validate end-to-end correctness | Cody Nguyen | 4/8/26 | Output file matches original input file |
| Run performance experiments | Ian Khoo | 4/8/26 | Completion times collected |
| Generate performance plots | Ian Khoo | 4/8/26 | Graphs produced for analysis |

### 10.2 Milestones

1. Sliding window sender implemented
2. Receiver correctly handles ordered and out-of-order packets
3. ACK corruption detection works correctly
4. DATA corruption detection works correctly
5. ACK packet loss recovery implemented
6. DATA packet loss recovery implemented
7. Completion time measurements collected across loss rates
8. Performance plots generated
9. Demo video(s) recorded

---

## 11 Demonstration Checklist

### Pre-Recording Checklist

**Phase 4 (Option 1):**
- [ ] Both terminal windows visible side-by-side

**Phase 4 (Option 2):**
- [ ] Both terminal windows visible side-by-side
- [ ] ACK corruption demonstration

**Phase 4 (Option 3):**
- [ ] Both terminal windows visible side-by-side
- [ ] DATA corruption demonstration

**Phase 4 (Option 4):**
- [ ] Both terminal windows visible side-by-side
- [ ] ACK packet loss demonstration

**Phase 4 (Option 5):**
- [ ] Both terminal windows visible side-by-side
- [ ] DATA packet loss demonstration
      
**Video Quality:**
- [ ] Both terminal windows visible side-by-side
- [ ] Clear explanation of steps
- [ ] Show file comparison/verification


