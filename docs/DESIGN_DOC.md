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
- Integrate and validate all three Phase 2(b)  scenarios (Options 1, 2, and 3) within the protocol logic.

**Workstream B: Olivia Pham**
- Design and implement the updated RDT 2.2 sender and receiver logic, including checksum validation, ACK handling, and retransmission behavior.

**Workstream C: Ian Khoo**
- Conduct performance evaluation experiments across all impairment levels.
- Generate completion-time plots and record demonstration videos for Phase 2.

---

## 3 Architecture and State Diagrams

### 3.1 State Diagram Evolution

#### Phase 2(a): RDT 2.2 File Transfer

```
Sender State Diagram:
                         +-------------------+
                         |   Wait for Call   |
                         |     (seq = 0)     |
                         +-------------------+
                                   |
                                   | rdt_send(data)
                                   | sndpkt = make_pkt(0, data, checksum)
                                   | udt_send(sndpkt)
                                   v
                         +-------------------+
              +--------->|  Wait for ACK 0   |<----------+
              |          +-------------------+           |
              |                    |                     |
              |                    | rcv valid ACK0      |
              |                    | seq = 1             |
              |                    v                     |
              |          +-------------------+           |
              |          |   Wait for Call   |           |
              |          |     (seq = 1)     |           |
              |          +-------------------+           |
              |                    |                     |
              |                    | rdt_send(data)      |
              |                    | sndpkt = make_pkt(1, data, checksum)
              |                    | udt_send(sndpkt)    |
              |                    v                     |
              |          +-------------------+           |
              +----------|  Wait for ACK 1   |-----------+
                         +-------------------+
                                   |
                                   | rcv valid ACK1
                                   | seq = 0
                                   v
                         (returns to Wait for Call 0)

Receiver State Diagram:
                         +-------------------+
              +--------->| Wait for Packet 0 |<----------+
              |          | (expected_seq=0)  |           |
              |          +-------------------+           |
              |               |           |               |
              |               |           +---------------+
              |               |           rcv corrupt pkt OR
              |               |           rcv pkt1
              |               |           sndpkt = make_pkt(ACK1, checksum)
              |               |           udt_send(sndpkt)
              |               |           [Stay in Wait for Packet 0]
              |               |
              |               | rcv valid pkt0
              |               | extract(data)
              |               | deliver_data(data)
              |               | sndpkt = make_pkt(ACK0, checksum)
              |               | udt_send(sndpkt)
              |               | expected_seq = 1
              |               v
              |          +-------------------+
              +----------|Wait for Packet 1  |-----------+
                         | (expected_seq=1)  |           |
                         +-------------------+           |
                                  |       |              |
                                  |       +--------------+
                                  |                      rcv corrupt pkt OR
                                  |                      rcv pkt0
                                  |                      sndpkt = make_pkt(ACK0, checksum)
                                  |                      udt_send(sndpkt)
                                  |                      [Stay in Wait for Packet 1]
                                  |
                                  | rcv valid pkt1
                                  | extract(data)
                                  | deliver_data(data)
                                  | sndpkt = make_pkt(ACK1, checksum)
                                  | udt_send(sndpkt)
                                  | expected_seq = 0
                                  v
                         (returns to Wait for Packet 0)

```

#### Phase 2(b): Error Injection and Recovery

```
Option 2 Corrupt ACK Packets:
Sender State Diagram (MODIFIED FOR OPTION 2):
                         +-------------------+
                         |   Wait for Call   |
                         |     (seq = 0)     |
                         +-------------------+
                                   |
                                   | rdt_send(data)
                                   | sndpkt = make_pkt(0, data, checksum)
                                   | udt_send(sndpkt)
                                   v
                         +-------------------+
              +--------->|  Wait for ACK 0   |<----------+
              |          +-------------------+           |
              |                    |                     |
              |                    | rcv ACK             |
              |                    | ┌─────────────────────────────────┐
              |                    | │ [OPTION 2 INJECTION]            │
              |                    | │ if should_corrupt_ack():        │
              |                    | │   rcvpkt = flip_bits(rcvpkt)    │
              |                    | └─────────────────────────────────┘
              |                    | validate_checksum(rcvpkt)
              |                    | parse_ack_num(rcvpkt)
              |                    |
              |                    | IF (NOT corrupt AND ack_num == 0):
              |                    |   seq = 1
              |                    |   [move to Wait for Call 1]
              |                    v
              |          +-------------------+
              |          |   Wait for Call   |
              |          |     (seq = 1)     |
              |          +-------------------+
              |                    |
              |                    | rdt_send(data)
              |                    | sndpkt = make_pkt(1, data, checksum)
              |                    | udt_send(sndpkt)
              |                    v
              |          +-------------------+
              +----------|  Wait for ACK 1   |-----------+
                         +-------------------+           |
                                   |                     |
                                   | rcv ACK             |
                                   | ┌─────────────────────────────────┐
                                   | │ [OPTION 2 INJECTION]            │
                                   | │ if should_corrupt_ack():        │
                                   | │   rcvpkt = flip_bits(rcvpkt)    │
                                   | └─────────────────────────────────┘
                                   | validate_checksum(rcvpkt)
                                   | parse_ack_num(rcvpkt)
                                   |
                                   | IF (NOT corrupt AND ack_num == 1):
                                   |   seq = 0
                                   |   [move to Wait for Call 0]
                                   v
                         (returns to Wait for Call 0)
Receiver State Diagram (MODIFIED FOR OPTION 2, though no differences from the original):
                         +-------------------+
              +--------->| Wait for Packet 0 |<----------+
              |          | (expected_seq=0)  |           |
              |          +-------------------+           |
              |               |           |               |
              |               |           +---------------+
              |               |           rcv corrupt pkt OR
              |               |           rcv pkt1
              |               |           sndpkt = make_pkt(ACK1, checksum)
              |               |           udt_send(sndpkt)
              |               |           [Stay in Wait for Packet 0]
              |               |
              |               | rcv valid pkt0
              |               | extract(data)
              |               | deliver_data(data)
              |               | sndpkt = make_pkt(ACK0, checksum)
              |               | udt_send(sndpkt)
              |               | expected_seq = 1
              |               v
              |          +-------------------+
              +----------|Wait for Packet 1  |-----------+
                         | (expected_seq=1)  |           |
                         +-------------------+           |
                                  |       |              |
                                  |       +--------------+
                                  |                      rcv corrupt pkt OR
                                  |                      rcv pkt0
                                  |                      sndpkt = make_pkt(ACK0, checksum)
                                  |                      udt_send(sndpkt)
                                  |                      [Stay in Wait for Packet 1]
                                  |
                                  | rcv valid pkt1
                                  | extract(data)
                                  | deliver_data(data)
                                  | sndpkt = make_pkt(ACK1, checksum)
                                  | udt_send(sndpkt)
                                  | expected_seq = 0
                                  v
                         (returns to Wait for Packet 0)

Option 3 Data bit-error:
Sender State Diagram (MODIFIED FOR OPTION 3, though no differences from the original):
                         +-------------------+
                         |   Wait for Call   |
                         |     (seq = 0)     |
                         +-------------------+
                                   |
                                   | rdt_send(data)
                                   | sndpkt = make_pkt(0, data, checksum)
                                   | udt_send(sndpkt)
                                   v
                         +-------------------+
              +--------->|  Wait for ACK 0   |<----------+
              |          +-------------------+           |
              |                    |                     |
              |                    | rcv valid ACK0      |
              |                    | seq = 1             |
              |                    v                     |
              |          +-------------------+           |
              |          |   Wait for Call   |           |
              |          |     (seq = 1)     |           |
              |          +-------------------+           |
              |                    |                     |
              |                    | rdt_send(data)      |
              |                    | sndpkt = make_pkt(1, data, checksum)
              |                    | udt_send(sndpkt)    |
              |                    v                     |
              |          +-------------------+           |
              +----------|  Wait for ACK 1   |-----------+
                         +-------------------+
                                   |
                                   | rcv valid ACK1
                                   | seq = 0
                                   v
                         (returns to Wait for Call 0)

Receiver State Diagram (MODIFIED FOR OPTION 3):
                         +-------------------+
              +--------->| Wait for Packet 0 |<----------+
              |          | (expected_seq=0)  |           |
              |          | last_ack_num=1    |           |
              |          +-------------------+           |
              |               |           |               |
              |               |           +---------------+
              |               |           rcv DATA
              |               |           ┌─────────────────────────────────┐
              |               |           │ [OPTION 3 INJECTION]            │
              |               |           │ if should_corrupt_data():       │
              |               |           │   rcvpkt = flip_bits(rcvpkt)    │
              |               |           └─────────────────────────────────┘
              |               |           validate_checksum(rcvpkt)
              |               |           parse_seq_num(rcvpkt)
              |               |           
              |               |           IF (corrupt OR seq_num == 1):
              |               |             sndpkt = make_pkt(ACK, last_ack_num)
              |               |             udt_send(sndpkt)
              |               |             [Send LAST valid ACK = ACK1]
              |               |             [Stay in Wait for Packet 0]
              |               |
              |               | rcv DATA
              |               | ┌─────────────────────────────────┐
              |               | │ [OPTION 3 INJECTION]            │
              |               | │ if should_corrupt_data():       │
              |               | │   rcvpkt = flip_bits(rcvpkt)    │
              |               | └─────────────────────────────────┘
              |               | validate_checksum(rcvpkt)
              |               | parse_seq_num(rcvpkt)
              |               |
              |               | IF (NOT corrupt AND seq_num == 0):
              |               |   extract(data)
              |               |   deliver_data(data)
              |               |   sndpkt = make_pkt(ACK0, checksum)
              |               |   udt_send(sndpkt)
              |               |   last_ack_num = 0
              |               |   expected_seq = 1
              |               v
              |          +-------------------+
              +----------|Wait for Packet 1  |-----------+
                         | (expected_seq=1)  |           |
                         | last_ack_num=0    |           |
                         +-------------------+           |
                                  |       |              |
                                  |       +--------------+
                                  |                      rcv DATA
                                  |                      ┌─────────────────────────────────┐
                                  |                      │ [OPTION 3 INJECTION]            │
                                  |                      │ if should_corrupt_data():       │
                                  |                      │   rcvpkt = flip_bits(rcvpkt)    │
                                  |                      └─────────────────────────────────┘
                                  |                      validate_checksum(rcvpkt)
                                  |                      parse_seq_num(rcvpkt)
                                  |                      
                                  |                      IF (corrupt OR seq_num == 0):
                                  |                        sndpkt = make_pkt(ACK, last_ack_num)
                                  |                        udt_send(sndpkt)
                                  |                        [Send LAST valid ACK = ACK0]
                                  |                        [Stay in Wait for Packet 1]
                                  |
                                  | rcv DATA
                                  | ┌─────────────────────────────────┐
                                  | │ [OPTION 3 INJECTION]            │
                                  | │ if should_corrupt_data():       │
                                  | │   rcvpkt = flip_bits(rcvpkt)    │
                                  | └─────────────────────────────────┘
                                  | validate_checksum(rcvpkt)
                                  | parse_seq_num(rcvpkt)
                                  |
                                  | IF (NOT corrupt AND seq_num == 1):
                                  |   extract(data)
                                  |   deliver_data(data)
                                  |   sndpkt = make_pkt(ACK1, checksum)
                                  |   udt_send(sndpkt)
                                  |   last_ack_num = 1
                                  |   expected_seq = 0
                                  v
                         (returns to Wait for Packet 0)
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
    SENDER                                              RECEIVER
    ======                                              ========
    
    seq = 0                                             expected_seq = 0
    |                                                   |
    | Create pkt0                                       |
    | Checksum: 0xAB12                                  |
    |                                                   |
    |------------- DATA(seq=0, "chunk0") -------------->|
    |              [Type='D', Seq=0, Len=1024]          |
    |              [Payload=chunk0, Checksum=0xAB12]    |
    |                                                   | Validate checksum ✓
    |                                                   | expected_seq == 0 ✓
    |                                                   | Deliver chunk0 to buffer[0]
    |                                                   | expected_seq = 1
    |                                                   |
    |<------------- ACK(ack_num=0) ---------------------|
    |              [Type='A', ACK=0, Checksum=0x1234]   |
    | Validate checksum ✓                               |
    | ACK matches seq ✓                                 |
    | seq = 1                                           |
    |                                                   |
    |                                                   |
    | Create pkt1                                       |
    | Checksum: 0xCD34                                  |
    |                                                   |
    |------------- DATA(seq=1, "chunk1") -------------->|
    |              [Type='D', Seq=1, Len=1024]          |
    |              [Payload=chunk1, Checksum=0xCD34]    |
    |                                                   | Validate checksum ✓
    |                                                   | expected_seq == 1 ✓
    |                                                   | Deliver chunk1 to buffer[1]
    |                                                   | expected_seq = 0
    |                                                   |
    |<------------- ACK(ack_num=1) ---------------------|
    |              [Type='A', ACK=1, Checksum=0x5678]   |
    | Validate checksum ✓                               |
    | ACK matches seq ✓                                 |
    | seq = 0                                           |
    |                                                   |
    |                                                   |
    | Create pkt0                                       |
    | Checksum: 0xEF56                                  |
    |                                                   |
    |------------- DATA(seq=0, "chunk2") -------------->|
    |              [Type='D', Seq=0, Len=1024]          |
    |              [Payload=chunk2, Checksum=0xEF56]    |
    |                                                   | Validate checksum ✓
    |                                                   | expected_seq == 0 ✓
    |                                                   | Deliver chunk2 to buffer[2]
    |                                                   | expected_seq = 1
    |                                                   |
    |<------------- ACK(ack_num=0) ---------------------|
    |              [Type='A', ACK=0, Checksum=0x9ABC]   |
    | Validate checksum ✓                               |
    | ACK matches seq ✓                                 |
    | seq = 1                                           |
    |                                                   |
    |                                                   |
    | Create pkt1                                       |
    | Checksum: 0x7890                                  |
    |                                                   |
    |------------- DATA(seq=1, "chunk3") -------------->|
    |              [Type='D', Seq=1, Len=1024]          |
    |              [Payload=chunk3, Checksum=0x7890]    |
    |                                                   | Validate checksum ✓
    |                                                   | expected_seq == 1 ✓
    |                                                   | Deliver chunk3 to buffer[3]
    |                                                   | expected_seq = 0
    |                                                   |
    |<------------- ACK(ack_num=1) ---------------------|
    |              [Type='A', ACK=1, Checksum=0xDEF0]   |
    | Validate checksum ✓                               |
    | ACK matches seq ✓                                 |
    | seq = 0                                           |
    |                                                   |
    | Transfer complete!                                | File reconstruction complete!
    | 4 packets sent                                    | 4 packets received
    | 0 retransmissions                                 | Write output.bmp

```

#### Phase 2(b): Error Injection and Recovery

```
Option 2 Corrupt ACK Packet w/ example data: 
    SENDER                                              RECEIVER
    ======                                              ========
    
    seq = 0                                             expected_seq = 0
    |                                                   |
    | Create pkt0                                       |
    |                                                   |
    |------------- DATA(seq=0, "chunk0") -------------->|
    |              Checksum=0xAB12                      |
    |                                                   | Validate checksum ✓
    |                                                   | Deliver chunk0
    |                                                   | expected_seq = 1
    |                                                   |
    |<------------- ACK(ack_num=0) ---------------------|
    |              Checksum=0x1234                      |
    | Validate checksum ✓                               |
    | seq = 1                                           |
    |                                                   |
    |                                                   |
    | Create pkt1                                       |
    |                                                   |
    |------------- DATA(seq=1, "chunk1") -------------->|
    |              Checksum=0xCD34                      |
    |                                                   | Validate checksum ✓
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
    | Validate checksum ✗ FAIL!                         |
    | Corrupt ACK detected                              |
    | Retransmit packet 1                               |
    |                                                   |
    |                                                   |
    |------------- DATA(seq=1, "chunk1") -------------->|
    |              [RETRANSMISSION]                     |
    |              Checksum=0xCD34                      |
    |                                                   | Validate checksum ✓
    |                                                   | seq == expected_seq? NO (dup)
    |                                                   | Already have chunk1
    |                                                   | Resend ACK1
    |                                                   |
    |<------------- ACK(ack_num=1) ---------------------|
    |              Checksum=0x5678                      |
    | Validate checksum ✓                               |
    | ACK matches seq ✓                                 |
    | seq = 0                                           |
    |                                                   |
    |                                                   |
    | Create pkt0                                       |
    |                                                   |
    |------------- DATA(seq=0, "chunk2") -------------->|
    |              Checksum=0xEF56                      |
    |                                                   | Validate checksum ✓
    |                                                   | Deliver chunk2
    |                                                   | expected_seq = 1
    |                                                   |
    |<------------- ACK(ack_num=0) ---------------------|
    | Validate checksum ✓                               |
    | seq = 1                                           |
    |                                                   |
    | Transfer complete!                                | File reconstruction complete!
    | 3 packets sent                                    | 3 unique packets received
    | 1 retransmission                                  |

Option 3 Data bit-Error w/ example data:
    SENDER                                              RECEIVER
    ======                                              ========
    
    seq = 0                                             expected_seq = 0
    |                                                   |
    | Create pkt0                                       |
    |                                                   |
    |------------- DATA(seq=0, "chunk0") -------------->|
    |              Checksum=0xAB12                      |
    |                                                   | Validate checksum ✓
    |                                                   | Deliver chunk0
    |                                                   | expected_seq = 1
    |                                                   | last_ack = 0
    |                                                   |
    |<------------- ACK(ack_num=0) ---------------------|
    | Validate checksum ✓                               |
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
    |                                                   | Validate checksum ✗ FAIL!
    |                                                   | Corrupt DATA detected
    |                                                   | Send last valid ACK (ACK0)
    |                                                   | Do NOT deliver data
    |                                                   | Do NOT change expected_seq
    |                                                   |
    |<------------- ACK(ack_num=0) ---------------------|
    |              [Last valid ACK]                     |
    | Validate checksum ✓                               |
    | Wrong ACK! (Expected ACK1, got ACK0)              |
    | Retransmit packet 1                               |
    |                                                   |
    |                                                   |
    |------------- DATA(seq=1, "chunk1") -------------->|
    |              [RETRANSMISSION]                     |
    |              Checksum=0xCD34                      |
    |                                                   | Validate checksum ✓
    |                                                   | expected_seq == 1 ✓
    |                                                   | Deliver chunk1
    |                                                   | expected_seq = 0
    |                                                   | last_ack = 1
    |                                                   |
    |<------------- ACK(ack_num=1) ---------------------|
    | Validate checksum ✓                               |
    | ACK matches seq ✓                                 |
    | seq = 0                                           |
    |                                                   |
    |                                                   |
    | Create pkt0                                       |
    |                                                   |
    |------------- DATA(seq=0, "chunk2") -------------->|
    |              Checksum=0xEF56                      |
    |                                                   | Validate checksum ✓
    |                                                   | Deliver chunk2
    |                                                   | expected_seq = 1
    |                                                   |
    |<------------- ACK(ack_num=0) ---------------------|
    | Validate checksum ✓                               |
    | seq = 1                                           |
    |                                                   |
    | Transfer complete!                                | File reconstruction complete!
    | 3 packets sent                                    | 3 unique packets received
    | 1 retransmission                                  |

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

**RDT 2.2 Packet Structure** (in `packet.py`)

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
|-- sender.py       	# Phase 2(a): RDT 2.2 file sender
|-- receiver.py   	 	# Phase 2(a): RDT 2.2 file receiver
|-- packet.py  			# Phase 2(a): DATA/ACK packet creation, parsing, and checksum utilities
|-- channel.py			# Phase 2(b): Bit-error injection and unreliable channel simulation 
|-- experiments.py		# Phase 2(c): Completion-time experiments and data collection
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

**Phase 2(a) - RDT 2.2 File Transfer**

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

**Phase 2(a) Sender Pseudocode:**

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

**Phase 2(b) - Error Injection and Recovery**

Steps:
1. Enable error injection based on option 1, 2, or 3 (ACK/DATA corruption)
2. After sending a DATA packet, wait for an ACK
3. If the ACK is corrupted, invalid, or times out:
	a. Retransmit the previously sent DATA packet
4. Continue retransmission until a valid ACK is received
5. Only advance the sequence number after successful ACK validation
	
**Phase 2(b) Pseudocode:**

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

**Phase 2(a) - RDT 2.2 File Transfer**
Steps:
1. Bind UDP socket to the receiver port
2. Initialize the expected sequence number
3. Initialize a buffer for storing received payloads
4. Loop until all packets are received:
	a. Receive a DATA packet
	b. Validate the checksum and sequence number
	c. If the packet is valid and matches the expected sequence number:
		i. Deliver the payload and store it
		ii. Send an ACK for the received sequence number
		iii. Toggle the expected sequence number
	d. Otherwise, resend the last valid ACK

**Phase 2(a) Receiver Pseudocode:**

```
initialize expected_seq = 0
initialize last_ack = ACK(1)
initialize received_count = 0

while received_count < total_packets do
    receive packet from UDP

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

**Phase 2(b) - Error Injection and Recovery**
Steps:
1. Enable DATA bit-error injection if configured
2. Once receiving corrupted DATA packet:
	a. Discard the packet
	b. Send the last valid ACK
3. Once receiving a duplicate DATA packet:
	a. Do not deliver the payload
	b. Send the last valid ACK
4. Continue as normal once a valid packet is received

**Phase 2(b) Receiver Pseudocode:**

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
During Phase 2(b):
ACK packet Bit error - ACK packet will be intentionally changed at the sender 
	-ACK will be changed randomly.
Data packet bit error - Data packet will be intentionally changed at the receiver
	-Bits will be shuffled, flipped, or randomized.

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
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

### 8.2 Tests
- 

**Integration Tests:**
- 

### 8.3 Test Artifacts
- 

---

## 9 Repository Structure and Reproducibility
WILL BE MORE UP-TO-DATE AFTER CODE
```
project/
|-- src/
|	|--
|
|-- tests/
|	|--
|
|-- scripts/
|	|--
|
|-- test_files/
|	|--
|
|-- results/
|	|--
|
|-- docs/
|   |-- DESIGN_DOC.md      # This document
|
|-- README.md
```

**To reproduce:**
```

```

---

## 10 Team Plan, Ownership, and Milestones

### 10.1 Task Ownership

| Task | Owner | Target Date | Definition of Done |
|---|---|---|---|
| Implement RDT 2.2 sender loop | Olivia Pham | 2/20/26 | Sender transmits DATA packets with alternating-bit seq, waits for ACK before advancing, and supports configurable timeout. |
| Implement ACK validation + retransmission logic | Olivia Pham | 2/20/26 | Sender correctly detects corrupt/wrong-seq ACKs and retransmits the last DATA packet until a valid ACK is received. |
| Implement RDT 2.2 receiver accept/duplicate/corrupt handling | Olivia Pham | 2/20/26 | Receiver validates checksum, delivers only expected seq packets, discards corrupt/duplicate packets, and responds with correct ACK or last ACK. |
|  |  | 2/20/26 |  |
|  |  | 2/20/26 |  |
|  |  | 2/20/26 |  |
| Collect completion time measurements in 5% increments | Ian Khoo | 2/20/26 | Measurements are collected |
| Generate plot of collected data | Ian Khoo | 2/20/26 | Plot is generated and sharable |

### 10.2 Milestones

1.  ACK is successfully implemented into the sender/receiver logic
2.  Receiver/Sender is able to detect and validate errors
3.  ACK packet bit error is correctly changing the data of ACK
4.  The data packet bit error is correctly changing the data of the data packet
5.  Completion time measurements are collected, and each impairment rate is tested with 5 independent runs, with results averaged.
6.  Plot with all data from completion time is generated
7.  Videos of working code are taken.

---

## 11 Demonstration Checklist

### Pre-Recording Checklist

**Phase 2(a):**
- [ ] Both terminal windows visible side-by-side

**Phase 2(b):**
- [ ] Both terminal windows visible side-by-side
- [ ] Terminal that shows error injection open

**Phase 2(c):**
- [ ] Both terminal windows visible side-by-side

**Video Quality:**
- [ ] Both terminal windows visible side-by-side
- [ ] Clear explanation of steps
- [ ] Show file comparison/verification


