# Network Design Project – Phase Proposal & Design Document 
## (Phase 5 of 5)

**Team Name:**  Don't Be COI

**Members:** 
- Cody Nguyen: cody_nguyen@student.uml.edu
- Olivia Pham: olivia_pham@student.uml.edu
- Ian Khoo: ian_khoo@student.uml.edu

**GitHub Repo URL (with GitHub usernames):** https://github.com/olitranpham/network-design, olitranpham, iantkhoo1488, codynguyen-dev

**Phase:** 5

**Submission Date:**  4/17/2026

**Version:** v6

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

**Phase 5(a):** TCP-style connection establishment using a simplified three-way handshake (SYN, SYN-ACK, ACK) before data transmission begins.

**Phase 5(b):** Dynamic sender window behavior based on congestion control and receiver-advertised flow control.

**Phase 5(c):** Implementation of TCP congestion control mechanisms including:
	- Slow start
	- Congestion avoidance
	- TCP Reno fast retransmit
	- TCP Reno fast recovery
	
**Phase 5(d):** Receiver-side flow control where the receiver advertises available buffer space (rwnd) and the sender limits transmission based on that window.

**Phase 5(e):** TCP-style connection teardown using a FIN/ACK exchange to reliably close the connection after file transfer.

---

## 1 Phase Requirements

### 1.1 Demo Deliverable

- **Private YouTube link **
	- Link: (https://youtu.be/5e1QwMdtTuE)
		- Timestamped outline:
			- Phase 5 Option 1 ==> 0:00 - 0:13
     		- Phase 5 Option 2 ==> 0:14 - 0:38
     		- Phase 5 Option 3 ==> 0:39 - 2:22
     		- Phase 5 Option 4 ==> 2:23 - 2:46
       		- Phase 5 Option 5 ==> 2:47 - 5:00
            - Phase 5 Generated Plots ==> 5:01 - 5:33

### 1.2 Required Demo Scenarios

**Phase 5(a) - TCP Connection Setup**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
| The two terminals are set up to show TCP connection  | Two terminals displaying information  | Both terminals should show they have established a connection  | The video shows the TCP connection at the start of each demo option  | 

**Phase 5(b) - Dynamic Sender Window**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
| Sender shifts window to allow for different packets to be sent  | window is set up, and is recomputed each iteration in relation to congestion events  | the window should grow and shrink in accordance with congestion  | The printout lines on the terminal show the window  |

**Phase 5(c) - TCP Slow Start Behavior**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
| Starts slowly, but as more ACKs come in, start sending more  | starts with cwnd at 1.0 and increments exponentially as ACKs come in  | it should increase the sending rate as time progresses  | The terminal shows the rate at which the sender is working; it can be visually seen as increasing  | 

**Phase 5(d) - Reno Fast Retransmit / Fast Recovery**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
| Activates on triple duplicate ACK  | on a triple duplicate ACK, each additional ACK after this will inflate cwnd by 1  | should allow for faster recovery if a packet is being consistently lost  | the video shows this in the terminal, and can be seen if a packet fails to ACK more than 3 times | 

**Phase 5(e) - Timeout-Based Congestion Response**

| Scenario | Configuration | Expected Behavior | What Video Will Show |
|---|---|---|---|
| On timeout, the system should perform timeout-based congestion response  | if a timeout occurs, it resets the fast-recovery and retransmits the entire window  | should activate and retransmit the window upon a timeout  | shown in the terminal when a timeout occurs  | 


### 1.3 Required Figures/Plots

Plot generated and included. 

---

## 2 Phase Plan

### 2.1 Scope

**New behaviors added:** 
- TCP-style connection establishment (three-way handshake)  
- TCP-style connection teardown (FIN handshake)  
- Dynamic congestion window (`cwnd`)  
- Receiver advertised window (`rwnd`)  
- Sender transmission limited by min(`cwnd`, `rwnd`)  
- Slow start congestion control  
- Congestion avoidance behavior  
- TCP Reno fast retransmit and fast recovery  

**Behaviors unchanged from previous phase:** 
- UDP socket communication
- Packet checksum validation
- File segmentation into 1024-byte chunks
- Error injection mechanisms
- Sliding window transmission framework  

**Out of scope (explicitly):**
- Selective acknowledgments (SACK)  
- Multiple simultaneous connections  
- Byte-level TCP sequence numbering  
- Advanced RTT estimation algorithms

### 2.2 Acceptance Criteria 

**Phase 5(a):**
- [ ] The sender initiates a connection using a SYN segment.
- [ ] The receiver responds with a SYN-ACK segment.
- [ ] The sender completes the handshake by sending an ACK segment.
- [ ] The connection enters the ESTABLISHED state before any data transfer occurs.
- [ ] If a handshake packet is lost, the sender retransmits the SYN after timeout.

**Phase 5(b):**
- [ ] The sender maintains a congestion window `(cwnd)`.
- [ ] The receiver advertises its available receive window `(rwnd)`.
- [ ] The sender limits transmission to `send_window = min(cwnd, rwnd)`
- [ ] The sender stops transmitting when the window is full.
- [ ] Transmission resumes when ACKs are received and the window advances.

**Phase 5(c):**
- [ ] The sender initializes `cwnd = 1`.
- [ ] For each ACK received during slow start, cwnd increases by 1 segment.
- [ ] `cwnd` grows exponentially until it reaches `ssthresh`.
- [ ] Once `cwnd >= ssthresh`, the sender transitions into congestion avoidance.
- [ ] The console output or logs show the growth of `cwnd`.

**Phase 5(d):**
- [ ] The sender tracks duplicate ACKs.
- [ ] When three duplicate ACKs are received, the sender immediately retransmits the missing segment.
- [ ] The sender updates congestion parameters `ssthresh = cwnd / 2` and `cwnd = ssthresh + 3`
- [ ] The sender enters fast recovery instead of waiting for timeout.
- [ ] Normal transmission resumes when the missing packet is acknowledged.
      
**Phase 5(e):**
- [ ] If a packet is lost and no ACK is received within the timeout interval, the sender retransmits the missing packet.
- [ ] Congestion control parameters are updated: `ssthresh = cwnd / 2` and `cwnd = 1`.
- [ ] The sender re-enters slow start after timeout.
- [ ] The file transfer continues until all packets are acknowledged.
      
**General:**
- [ ] README.md is complete
- [ ] Invite instructor(s) to GitHub repo and include GitHub link
- [ ] Record demo and upload to YouTube 

### 2.3 Work Breakdown

**New Tasks for Phase 5:**
- Implement TCP-style connection establishment using a three-way handshake (SYN, SYN-ACK, ACK).
- Extend the existing Go-Back-N data transfer system to support a TCP-like dynamic sliding window.
- Implement congestion control mechanisms, including slow start and congestion avoidance.
- Implement TCP Reno fast retransmit and fast recovery triggered by duplicate ACKs.
- Implement receiver-advertised flow control (rwnd) and enforce sender limits based on min(cwnd, rwnd).
- Implement timeout-based congestion response, including updating cwnd and ssthresh.
- Implement TCP-style connection teardown using a FIN/ACK exchange.
- Test protocol behavior under all required demo scenarios (Options 1–5).
- Generate performance graphs including completion time under packet loss and congestion window evolution.

**Workstream A: Cody Nguyen**
- Integrate TCP-style connection setup and teardown into the existing UDP communication framework.
- Implement and validate packet loss and duplicate ACK scenarios used in Options 4 and 5.
- Ensure sender correctly detects duplicate ACKs and triggers fast retransmit.
- Validate retransmission behavior under packet loss and timeout conditions.

**Workstream B: Olivia Pham**
- Extend the sender architecture to support TCP-style congestion control.
- Implement congestion window `(cwnd)` tracking and updates during slow start and congestion avoidance.
- Implement logic to compute the effective sending window `min(cwnd, rwnd)`.
- Implement timeout handling that updates `ssthresh` and resets `cwnd`.
- Integrate the new congestion-control logic with the existing reliable data transfer system.
  
**Workstream C: Ian Khoo**
- Conduct performance experiments across varying packet loss probabilities.
- Measure completion times and evaluate the impact of congestion control mechanisms.
- Track congestion window `(cwnd)` evolution during transfers.
- Generate required plots for Phase 5 performance analysis.
- Record demonstration videos for all Phase 5 scenarios.

---

## 3 Architecture and State Diagrams

### 3.1 State Diagram Evolution

#### Phase 5(a): TCP Connection Establishment (Three-Way Handshake)

```
Sender (Client) State Diagram:
                         +-----------------------------+
                         |          CLOSED             |
                         +-----------------------------+
                                        |
                                        | connect()
                                        | sndpkt = make_pkt(SYN, seq=0, checksum)
                                        | udt_send(sndpkt)
                                        | start_timer()
                                        v
                         +-----------------------------+
              +--------->|          SYN_SENT           |
              |          +-----------------------------+
              |               |              |
              |               | timeout      | rcv SYN-ACK
              |               | retransmit   | validate_checksum(rcvpkt)
              |               | SYN          |
              |               | restart_     | IF (NOT corrupt):
              +---------------+ timer()      |   sndpkt = make_pkt(ACK, seq=1, checksum)
                                             |   udt_send(sndpkt)
                                             |   stop_timer()
                                             v
                         +-----------------------------+
                         |         ESTABLISHED         |
                         |   base = 0                  |
                         |   next_seq_num = 0          |
                         |   cwnd = 1                  |
                         |   ssthresh = 16             |
                         |   dup_ack_count = 0         |
                         |   send_window = min(cwnd,   |
                         |                    rwnd)    |
                         +-----------------------------+
                                        |
                                        | [proceed to Phase 5(b)]


Receiver (Server) State Diagram:
                         +-----------------------------+
                         |           LISTEN            |
                         +-----------------------------+
                                        |
                                        | rcv SYN
                                        | validate_checksum(rcvpkt)
                                        |
                                        | IF corrupt: [ignore, stay]
                                        |
                                        | IF (NOT corrupt):
                                        |   sndpkt = make_pkt(SYN-ACK, seq=0, checksum)
                                        |   udt_send(sndpkt)
                                        v
                         +-----------------------------+
              +--------->|          SYN_RCVD           |
              |          +-----------------------------+
              |               |
              |               | rcv ACK
              |               | validate_checksum(rcvpkt)
              |               |
              |               | IF corrupt: [ignore, stay]
              +---------------+
                              |
                              | IF (NOT corrupt):
                              v
                         +-----------------------------+
                         |         ESTABLISHED         |
                         |   expected_seq_num = 0      |
                         |   last_ack_num = -1         |
                         |   rwnd = RECV_BUFFER_SIZE   |
                         +-----------------------------+
                                        |
                                        | [proceed to Phase 5(c)]
```

#### Phase 5(b): TCP Dynamic Sender Window Behavior

```
Sender State Diagram:
                         +-----------------------------+
                         |         ESTABLISHED         |
                         |   base = 0                  |
                         |   next_seq_num = 0          |
                         |   cwnd = 1                  |
                         |   ssthresh = 16             |
                         |   dup_ack_count = 0         |
                         |   rwnd = (from receiver)    |
                         |   send_window =             |
                         |     min(cwnd, rwnd)         |
                         +-----------------------------+
                                        |
                                        | rdt_send(data)
                                        | [next_seq_num < base + send_window]
                                        | sndpkt[next_seq_num] = make_pkt(next_seq_num, data, checksum)
                                        | udt_send(sndpkt[next_seq_num])
                                        | if base == next_seq_num: start_timer()
                                        | next_seq_num++
                                        v
                         +-----------------------------+
              +--------->|    Wait for ACK / Timeout   |<----------+
              |          +-----------------------------+           |
              |               |                    |               |
              |               |                    | timeout       |
              |               |                    | [TIMEOUT:     |
              |               |                    |  see Phase    |
              |               |                    |  5(d)]        |
              |               |                    +---------------+
              |               |
              |               | rcv ACK(n, rwnd_adv)
              |               | validate_checksum(rcvpkt)
              |               | parse_ack_num(rcvpkt)
              |               | parse_rwnd(rcvpkt)
              |               |
              |               | IF corrupt: [ignore, stay]
              |               |
              |               | IF (NOT corrupt AND n == base - 1):
              |               |   dup_ack_count++
              |               |   [duplicate ACK: see Phase 5(d)]
              |               |
              |               | IF (NOT corrupt AND n >= base):
              |               |   base = n + 1
              |               |   rwnd = rwnd_adv
              |               |   send_window = min(cwnd, rwnd)
              |               |   [update cwnd: see Phase 5(d)]
              |               |   dup_ack_count = 0
              |               |   if base == next_seq_num:
              |               |     stop_timer()
              |               |   else:
              |               |     restart_timer()
              |               |   [send new pkts while eligible]
              +---------------+
```

#### Phase 5(c): TCP Receiver Behavior and Flow Control

```
Receiver State Diagram:
                         +-----------------------------+
              +--------->|    Wait for Packet          |<----------+
              |          |   expected_seq_num = 0      |           |
              |          |   last_ack_num = -1         |           |
              |          |   rwnd = RECV_BUFFER_SIZE   |           |
              |          +-----------------------------+           |
              |               |              |                     |
              |               |              +---------------------+
              |               |              rcv corrupt pkt OR
              |               |              rcv out-of-order pkt
              |               |              (seq != expected_seq_num)
              |               |              rwnd = RECV_BUFFER_SIZE - buffered
              |               |              sndpkt = make_pkt(ACK, last_ack_num,
              |               |                                   rwnd, checksum)
              |               |              udt_send(sndpkt)
              |               |              [discard pkt, stay]
              |               |
              |               | rcv valid pkt (NOT corrupt AND
              |               |               seq == expected_seq_num)
              |               | extract(data)
              |               | deliver_data(data)
              |               | last_ack_num = expected_seq_num
              |               | rwnd = RECV_BUFFER_SIZE - buffered
              |               | sndpkt = make_pkt(ACK, expected_seq_num,
              |               |                        rwnd, checksum)
              |               | udt_send(sndpkt)
              |               | expected_seq_num++
              +---------------+

```

#### Phase 5(d): Congestion Control and Loss Recovery

```
Congestion Control State Diagram:
                         +-----------------------------+
                         |         SLOW START          |
                         |   cwnd = 1                  |
                         |   ssthresh = 16 (initial)   |
                         +-----------------------------+
                                        |
                                        | rcv new ACK (n >= base)
                                        | cwnd = cwnd + 1
                                        | [exponential growth per ACK]
                                        |
                              +---------+----------+
                              |                    |
                              | cwnd < ssthresh    | cwnd >= ssthresh
                              | [stay in           v
                              |  slow start]  +-----------------------------+
                              +-------------->|    CONGESTION AVOIDANCE     |
                                              +-----------------------------+
                                                   |
                                                   | rcv new ACK (n >= base)
                                                   | cwnd = cwnd + (1 / cwnd)
                                                   | [approx +1 segment per RTT]
                                                   |
                                 +-----------------+
                                 |
                                 | 3 duplicate ACKs received
                                 | [FAST RETRANSMIT]
                                 v
                         +-----------------------------+
              +--------->|       FAST RECOVERY         |
              |          |   ssthresh = max(cwnd/2, 2) |
              |          |   cwnd = ssthresh + 3       |
              |          |   retransmit sndpkt[base]   |
              |          +-----------------------------+
              |               |              |
              |               | rcv another  | rcv new ACK
              |               | dup ACK      | (n > base - 1)
              |               | cwnd++       | [FAST RECOVERY EXIT]
              |               | [send new    | base = n + 1
              |               |  pkt if      | cwnd = ssthresh
              |               |  window      | dup_ack_count = 0
              +---------------+ allows]      | restart or stop timer
                                             v
                         +-----------------------------+
                         |    CONGESTION AVOIDANCE     |
                         |    (resume)                 |
                         +-----------------------------+

              Timeout (from any state above):
              +-----------------------------+
              |   [TIMEOUT LOSS RECOVERY]   |
              |   ssthresh = max(cwnd/2, 2) |
              |   cwnd = 1                  |
              |   dup_ack_count = 0         |
              |   retransmit ALL            |
              |     sndpkt[base..           |
              |     next_seq_num-1]         |
              |   restart_timer()           |
              +-----------------------------+
                              |
                              v
                         +-----------------------------+
                         |      SLOW START (re-enter)  |
                         +-----------------------------+


```

### Phase 5(e): TCP Connection Teardown (FIN/ACK Exchange)

```
Sender (Active Close) State Diagram:
                         +-----------------------------+
                         |         ESTABLISHED         |
                         |   [all data sent and ACKed] |
                         +-----------------------------+
                                        |
                                        | close()
                                        | sndpkt = make_pkt(FIN, seq=next_seq_num,
                                        |                        checksum)
                                        | udt_send(sndpkt)
                                        | start_timer()
                                        v
                         +-----------------------------+
              +--------->|          FIN_WAIT           |
              |          +-----------------------------+
              |               |              |
              |               | timeout      | rcv FIN-ACK
              |               | retransmit   | validate_checksum(rcvpkt)
              |               | FIN          |
              |               | restart_     | IF (NOT corrupt):
              +---------------+ timer()      |   sndpkt = make_pkt(ACK, checksum)
                                             |   udt_send(sndpkt)
                                             |   stop_timer()
                                             v
                         +-----------------------------+
                         |           CLOSED            |
                         +-----------------------------+


Receiver (Passive Close) State Diagram:
                         +-----------------------------+
              +--------->|         ESTABLISHED         |
              |          |   [receiving data]          |
              |          +-----------------------------+
              |               |
              |               | rcv FIN
              |               | validate_checksum(rcvpkt)
              |               |
              |               | IF corrupt: [ignore, stay]
              +---------------+
                              |
                              | IF (NOT corrupt):
                              |   deliver_remaining_data()
                              |   sndpkt = make_pkt(FIN-ACK, checksum)
                              |   udt_send(sndpkt)
                              v
                         +-----------------------------+
              +--------->|         CLOSE_WAIT          |
              |          +-----------------------------+
              |               |
              |               | rcv ACK
              |               | validate_checksum(rcvpkt)
              |               |
              |               | IF corrupt: [ignore, stay]
              +---------------+
                              |
                              | IF (NOT corrupt):
                              v
                         +-----------------------------+
                         |           CLOSED            |
                         +-----------------------------+
```

### 3.2 Component Responsibilities

**Phase 5(a-e) - Sender Components**

`sender.py` Main Responsibilities:
- Initiate TCP-style connection setup using a three-way handshake (SYN, SYN-ACK, ACK).
- Read BMP file into memory.
- Compute the total number of packets using a fixed payload size 
- Divide BMP file data into chunks of 1024 bytes
- Packetize file and transmit using the Go-Back-N protocol
- Maintain sliding window variables
	- `seq_num`: Sequence number of the next packet to send
 	- `ack_num`: Acknowledgment number expected from the receiver
- Maintain congestion control parameters:
  - `cwnd` (congestion window)
  - `sstresh` (slow start threshold)
- Compute effective sending window `send_window = min(cwnd, rwnd)`
- Send packets while the sender window allows transmission.
- Start and manage retransmission timers.
- Process cumulative ACK packets received from the receiver
- Detect duplicate ACKs and trigger fast retransmit / fast recovery.
- Update congestion control parameters during slow start, congestion avoidance, and timeout events
- Retransmit missing packets when loss is detected.
- Print transmission progress into console
- Initiate connection teardown using a FIN/ACK exchange after file transfer completes.

**Phase 4(c-d) - Receiver Components**

`receiver.py` Main Responsibilities:
- Create and bind UDP socket to the receiver port
- Respond to connection setup by replying to SYN with SYN-ACK.
- Maintain receiver connection state.
- Receive TCP-like DATA packets and validate checksums.
- Maintain `expected_seq_num` for in-order packet reception.
- Accept and deliver packets only if `seq == expected_seq_num`
- Store payload data for file reconstruction.
- Send cumulative ACK packets for the last correctly received packet.
- Advertise available receiver window `(rwnd)` to support flow control.
- Discard out-of-order packets and resend the last ACK.
- For corrupt/unexpected DATA packets -> resend last valid ACK
- Respond to FIN packets and participate in TCP-style connection teardown.
- Write the reconstructed file to disk

**Shared Modules**
- `packet.py` - Packet encoding/decoding utilities
	- Define the TCP-like packet structure.
   	- Build and parse packet types: `SYN`, `ACK`, `DATA`, `FIN`.
	- Encode and decode packet header fields.
	- Compute packet checksum for error detection.
	- Provide packet structure utilities used by both sender and receiver.

### 3.3 Message Flow Overview

#### Phase 5(a): TCP Connection Establishment and Normal Transfer

```
SENDER                                              RECEIVER
    ======                                              ========

    CLOSED                                              LISTEN
    cwnd = 1, ssthresh = 16
    |                                                   |
    | [THREE-WAY HANDSHAKE]                             |
    |                                                   |
    |------------- SYN(seq=0) ------------------------->|
    |                                                   | rcv SYN, validate checksum
    | SYN_SENT                                          | SYN_RCVD
    |                                                   |
    |<------------- SYN-ACK(seq=0) --------------------|
    | rcv SYN-ACK, validate checksum                    |
    |------------- ACK(seq=1) ------------------------->|
    |                                                   | rcv ACK, validate checksum
    | ESTABLISHED                                       | ESTABLISHED
    | base=0, next_seq_num=0                            | expected_seq_num=0
    | send_window = min(cwnd=1, rwnd=N) = 1             | rwnd = N
    |                                                   |
    | [DATA TRANSFER — window grows via slow start]     |
    |                                                   |
    | Send pkt0 (send_window=1, window full)            |
    |------------- DATA(seq=0, "chunk0") -------------->|
    |                                                   | Validate checksum
    |                                                   | seq==expected(0), deliver chunk0
    |                                                   | expected_seq_num=1, rwnd=N
    |<------------- ACK(ack_num=0, rwnd=N) -------------|
    | base=1, cwnd=2, send_window=min(2,N)=2            |
    |                                                   |
    | Send pkt1 (window open)                           |
    |------------- DATA(seq=1, "chunk1") -------------->|
    | Send pkt2 (window open)                           | Validate checksum
    |------------- DATA(seq=2, "chunk2") -------------->| seq==expected(1), deliver chunk1
    |                                                   | expected_seq_num=2, rwnd=N
    |<------------- ACK(ack_num=1, rwnd=N) -------------|
    | base=2, cwnd=3, send_window=min(3,N)              |
    |<------------- ACK(ack_num=2, rwnd=N) -------------|
    | base=3, cwnd=4, send_window=min(4,N)              |
    |                                                   |
    | -------------- Continue until all data sent ----- |
    |                                                   |
    | [CONNECTION TEARDOWN]                             |
    |                                                   |
    |------------- FIN ------------------------------>  |
    |<------------- FIN-ACK --------------------------- |
    |------------- ACK ------------------------------>  |
    |                                                   |
    | CLOSED                                            | CLOSED
    | Transfer complete                                 | File reconstruction complete
    | n packets sent, 0 retransmission(s)               | Write output.bmp
```

#### Phase 5(b): Flow-Control-Limited Data Transfer

```
SENDER                                              RECEIVER
    ======                                              ========

    ESTABLISHED                                         ESTABLISHED
    base=0, next_seq_num=0                              expected_seq_num=0
    cwnd=4, ssthresh=16                                 rwnd=2  (receive buffer nearly full)
    send_window = min(cwnd=4, rwnd=2) = 2               last_ack_num=-1
    |                                                   |
    | send_window=2, only 2 pkts permitted              |
    |                                                   |
    | Send pkt0 (window open)                           |
    |------------- DATA(seq=0, "chunk0") -------------->|
    | Send pkt1 (window open)                           | Validate checksum
    |------------- DATA(seq=1, "chunk1") -------------->| seq==expected(0), deliver chunk0
    |                                                   | expected_seq_num=1
    | [window full: next_seq_num=2 == base+send_window] | rwnd=1 (buffer filling)
    | [SENDER BLOCKED — waiting for ACK]                |
    |                                                   |
    |<------------- ACK(ack_num=0, rwnd=1) -------------|
    | base=1                                            |
    | rwnd=1, send_window = min(cwnd=4, rwnd=1) = 1     |
    | [still flow-controlled: only 1 slot open]         |
    |                                                   | seq==expected(1), deliver chunk1
    | Send pkt2 (1 slot open)                           | expected_seq_num=2
    |------------- DATA(seq=2, "chunk2") -------------->| rwnd=0 (buffer full)
    |                                                   |
    |<------------- ACK(ack_num=1, rwnd=0) -------------|
    | base=2                                            |
    | rwnd=0, send_window = min(cwnd=4, rwnd=0) = 0     |
    | [SENDER BLOCKED — rwnd=0, zero window]            |
    |                                                   |
    | [Receiver drains buffer, frees space]             |
    |                                                   | deliver chunk2, buffer drained
    |                                                   | rwnd=3 (buffer freed)
    |<------------- ACK(ack_num=2, rwnd=3) -------------|
    | base=3                                            |
    | rwnd=3, send_window = min(cwnd=4, rwnd=3) = 3     |
    | [transmission resumes]                            |
    |                                                   |
    | Send pkt3 (window open)                           |
    |------------- DATA(seq=3, "chunk3") -------------->|
    | Send pkt4 (window open)                           |
    |------------- DATA(seq=4, "chunk4") -------------->|
    | Send pkt5 (window open)                           |
    |------------- DATA(seq=5, "chunk5") -------------->|
    |                                                   |
    | -------------- Continue until all data sent ----- |
    | Transfer complete                                 | File reconstruction complete
    | n packets sent, 0 retransmission(s)               | Write output.bmp
```

### Phase 5(c): Slow Start and Congestion Window Growth

```
SENDER                                              RECEIVER
    ======                                              ========

    ESTABLISHED                                         ESTABLISHED
    base=0, next_seq_num=0                              expected_seq_num=0
    cwnd=1, ssthresh=8, rwnd=16                         rwnd=16
    send_window = min(cwnd=1, rwnd=16) = 1
    |                                                   |
    | [SLOW START: cwnd < ssthresh]                     |
    |                                                   |
    | RTT 1: send_window=1                              |
    |------------- DATA(seq=0, "chunk0") -------------->|
    |                                                   | deliver chunk0, ACK0
    |<------------- ACK(ack_num=0, rwnd=16) ------------|
    | cwnd = cwnd + 1 = 2                               |
    | send_window = min(2,16) = 2                       |
    |                                                   |
    | RTT 2: send_window=2                              |
    |------------- DATA(seq=1, "chunk1") -------------->|
    |------------- DATA(seq=2, "chunk2") -------------->| deliver chunk1, ACK1
    |                                                   | deliver chunk2, ACK2
    |<------------- ACK(ack_num=1, rwnd=16) ------------|
    | cwnd = cwnd + 1 = 3                               |
    |<------------- ACK(ack_num=2, rwnd=16) ------------|
    | cwnd = cwnd + 1 = 4                               |
    | send_window = min(4,16) = 4                       |
    |                                                   |
    | RTT 3: send_window=4                              |
    |------------- DATA(seq=3, "chunk3") -------------->|
    |------------- DATA(seq=4, "chunk4") -------------->| deliver chunk3..6, ACK3..6
    |------------- DATA(seq=5, "chunk5") -------------->|
    |------------- DATA(seq=6, "chunk6") -------------->|
    |<------------- ACK(ack_num=3, rwnd=16) ------------|
    | cwnd=5                                            |
    |<------------- ACK(ack_num=4, rwnd=16) ------------|
    | cwnd=6                                            |
    |<------------- ACK(ack_num=5, rwnd=16) ------------|
    | cwnd=7                                            |
    |<------------- ACK(ack_num=6, rwnd=16) ------------|
    | cwnd=8 == ssthresh                                |
    |                                                   |
    | [TRANSITION: cwnd >= ssthresh]                    |
    | [Enter CONGESTION AVOIDANCE]                      |
    |                                                   |
    | RTT 4: send_window=8                              |
    |------------- DATA(seq=7..14) ------------------>  |
    |                                                   | deliver chunk7..14, ACK7..14
    |<------------- ACK(ack_num=7, rwnd=16) ------------|
    | cwnd = 8 + 1/8 = 8.125                            |
    |<------------- ACK(ack_num=8, rwnd=16) ------------|
    | cwnd = 8.125 + 1/8 ≈ 8.25                         |
    |        ... (8 ACKs total, cwnd ≈ 9 after RTT) ... |
    |<------------- ACK(ack_num=14, rwnd=16) -----------|
    | cwnd ≈ 9, send_window = min(9,16) = 9             |
    | [LINEAR growth continues]                         |
    |                                                   |
    | -------------- Continue until all data sent ----- |
    | Transfer complete                                 | File reconstruction complete
    | n packets sent, 0 retransmission(s)               | Write output.bmp
```

### Phase 5(d): Reno Fast Retransmit and Fast Recovery

```
SENDER                                              RECEIVER
    ======                                              ========

    ESTABLISHED                                         ESTABLISHED
    base=4, next_seq_num=9                              expected_seq_num=4
    cwnd=8, ssthresh=16, rwnd=16                        rwnd=16
    send_window = min(8,16) = 8, dup_ack_count=0
    |                                                   |
    |------------- DATA(seq=4, "chunk4") -------------->|
    |------------- DATA(seq=5, "chunk5") --------X      | pkt5 dropped in transit
    |------------- DATA(seq=6, "chunk6") -------------->|
    |------------- DATA(seq=7, "chunk7") -------------->|
    |------------- DATA(seq=8, "chunk8") -------------->|
    |                                                   |
    |                                                   | seq==expected(4), deliver chunk4
    |                                                   | ACK4, expected_seq_num=5
    |<------------- ACK(ack_num=4, rwnd=16) ------------|
    | base=5, dup_ack_count=0                           |
    |                                                   |
    |                                                   | seq=6 != expected(5), out-of-order
    |                                                   | Send last valid ACK (ACK4)
    |<------------- ACK(ack_num=4, rwnd=16) [dup 1] ----|
    | dup_ack_count=1                                   |
    |                                                   |
    |                                                   | seq=7 != expected(5), out-of-order
    |                                                   | Send last valid ACK (ACK4)
    |<------------- ACK(ack_num=4, rwnd=16) [dup 2] ----|
    | dup_ack_count=2                                   |
    |                                                   |
    |                                                   | seq=8 != expected(5), out-of-order
    |                                                   | Send last valid ACK (ACK4)
    |<------------- ACK(ack_num=4, rwnd=16) [dup 3] ----|
    | dup_ack_count=3                                   |
    |                                                   |
    | ┌─────────────────────────────────────────┐       |
    | │ FAST RETRANSMIT (3 dup ACKs)            │       |
    | │ ssthresh = max(cwnd/2, 2) = 4           │       |
    | │ cwnd = ssthresh + 3 = 7                 │       |
    | │ retransmit sndpkt[base=5] immediately   │       |
    | │ Enter FAST RECOVERY                     │       |
    | └─────────────────────────────────────────┘       |
    |                                                   |
    |------------- DATA(seq=5, "chunk5") [RETX] ------->|
    |                                                   |
    | [FAST RECOVERY: inflate cwnd per extra dup ACK]   |
    | [send new pkt if send_window allows]              |
    |                                                   | seq==expected(5), deliver chunk5
    |                                                   | ACK5, expected_seq_num=6
    |                                                   | seq==expected(6), deliver chunk6
    |                                                   | ACK6, expected_seq_num=7
    |                                                   | (buffered pkts 6,7,8 now deliverable)
    |                                                   | ACK7, ACK8
    |<------------- ACK(ack_num=5, rwnd=16) ------------|
    |                                                   |
    | ┌─────────────────────────────────────────┐       |
    | │ FAST RECOVERY EXIT (new ACK > base-1)   │       |
    | │ base = 6                                │       |
    | │ cwnd = ssthresh = 4                     │       |
    | │ dup_ack_count = 0                       │       |
    | │ Enter CONGESTION AVOIDANCE              │       |
    | └─────────────────────────────────────────┘       |
    |                                                   |
    |<------------- ACK(ack_num=6, rwnd=16) ------------|
    | base=7, cwnd = 4 + 1/4 ≈ 4.25                    |
    |<------------- ACK(ack_num=7, rwnd=16) ------------|
    | base=8, cwnd ≈ 4.5                                |
    |<------------- ACK(ack_num=8, rwnd=16) ------------|
    | base=9, cwnd ≈ 4.75                               |
    |                                                   |
    | -------------- Continue until all data sent ----- |
    | Transfer complete                                 | File reconstruction complete
    | n packets sent, x retransmission(s)               | Write output.bmp
```

### Phase 5(e): Timeout-Based Congestion Recovery

```
SENDER                                              RECEIVER
    ======                                              ========

    ESTABLISHED                                         ESTABLISHED
    base=3, next_seq_num=7                              expected_seq_num=3
    cwnd=6, ssthresh=16, rwnd=16                        rwnd=16
    send_window = min(6,16) = 6, dup_ack_count=0
    |                                                   |
    |------------- DATA(seq=3, "chunk3") -------------->|
    |------------- DATA(seq=4, "chunk4") -------------->|
    |------------- DATA(seq=5, "chunk5") -------------->|
    |------------- DATA(seq=6, "chunk6") -------------->|
    |                                                   |
    | ┌─────────────────────────────────────────┐       |
    | │ ERROR INJECTION (Option 4/5)            │       |
    | │ All ACKs lost in transit                │       |
    | └─────────────────────────────────────────┘       |
    |                                                   |
    |        X----- ACK(ack_num=3) lost ----------------|
    |        X----- ACK(ack_num=4) lost ----------------|
    |        X----- ACK(ack_num=5) lost ----------------|
    |        X----- ACK(ack_num=6) lost ----------------|
    |                                                   |
    | [No dup ACKs received — fast retransmit           |
    |  does NOT trigger]                                |
    |                                                   |
    | Timer expires (base=3 unACKed)                    |
    |                                                   |
    | ┌─────────────────────────────────────────┐       |
    | │ TIMEOUT CONGESTION RESPONSE             │       |
    | │ ssthresh = max(cwnd/2, 2) = 3           │       |
    | │ cwnd = 1                                │       |
    | │ dup_ack_count = 0                       │       |
    | │ Re-enter SLOW START                     │       |
    | └─────────────────────────────────────────┘       |
    |                                                   |
    | Retransmit ALL: pkt3, pkt4, pkt5, pkt6            |
    |------------- DATA(seq=3, "chunk3") [RETX] ------->|
    |------------- DATA(seq=4, "chunk4") [RETX] ------->| seq==expected(3), deliver chunk3
    |------------- DATA(seq=5, "chunk5") [RETX] ------->| seq==expected(4), deliver chunk4
    |------------- DATA(seq=6, "chunk6") [RETX] ------->| seq==expected(5), deliver chunk5
    |                                                   | seq==expected(6), deliver chunk6
    |                                                   |
    |<------------- ACK(ack_num=3, rwnd=16) ------------|
    | base=4                                            |
    | [SLOW START] cwnd = 1 + 1 = 2                     |
    | send_window = min(2,16) = 2                       |
    |<------------- ACK(ack_num=4, rwnd=16) ------------|
    | base=5, cwnd=3, send_window=3                     |
    |<------------- ACK(ack_num=5, rwnd=16) ------------|
    | base=6, cwnd=4, send_window=4                     |
    |<------------- ACK(ack_num=6, rwnd=16) ------------|
    | base=7, cwnd=5                                    |
    |                                                   |
    | [cwnd=5 >= ssthresh=3]                            |
    | [TRANSITION: Enter CONGESTION AVOIDANCE]          |
    | cwnd grows linearly: +1/cwnd per ACK              |
    |                                                   |
    | -------------- Continue until all data sent ----- |
    | Transfer complete                                 | File reconstruction complete
    | n packets sent, x retransmission(s)               | Write output.bmp
```

---

## 4 Packet Format

### 4.1 Packet Types
- DATA: carries file chunk with a sequence number
- ACK: cumulative acknowledgment indicating the highest in-order packet received
- SYN: initiates connection establishment
- SYN-ACK: acknowledges connection request
- FIN: initiates connection termination

### 4.2 Header Fields

| Field | Size (bytes/bits) | Type | Description | Notes |
|---|---|---|---|---|
| pkt_type | 1 | uint8 | O = DATA, 1 = ACK | Identifies packet type |
| seq | 4 | uint32 | DATA seq (0/1) or ACK number (0/1) | Used for Go-Back-N sliding window | 
| ack | 4 | uint32 | Acknowledgement number | Highest in-order packet received |
| rwnd | 2 | uint16 | Receiver advertised window | Used for flow control |
| payload_length | 2 | uint16 | DATA payload size (0 for ACK) |  |
| total_packets | 4 | uint32 | Total number of DATA packets |
| checksum | 4 | uint32 | Checksum over header and payload with checksum field = 0 during calculations | | 
| payload | ≤ 1024 | bytes | File data chunk | DATA only |

**Total header size:** 21 bytes
**Maximum packet size:** 21 + 1024 = 1045 bytes

**Encoding format (Python struct):**

```python
header_format = "!BIIHHII"
# type, seq, ack, rwnd, payload_len, total_packets, checksum
```

---

## 5 Data Structures and Module Map

### 5.1 Key Data Structures

**TCP-like Packet Structure** (in `packet.py`)

- Fields:
  - `pkt_type` (uint8): Packet type identifier (SYN / SYN-ACK / DATA / ACK / FIN)
  - `seq` (uint32): Sequence number used for ordered packet delivery
  - `ack` (uint32): Acknowledgment number representing the highest in-order packet received
  - `rwnd` (uint16): Receiver advertised window used for flow control
  - `payload_length`(uint16): Number of valid bytes in the payload (0 for ACK packets)
  - `total_packets` (uint32): Total number of DATA packets in the transfer
  - `checksum` (uint32): Checksum computer over header and payload
  - `payload` (bytes): File data chunk (up to 1024 bytes)

- Invariants:
  - `0 <= payload_length <= 1024`
  - `total_packets >= 1`
  - Control packets (SYN / ACK / FIN) contain no payload

**Sender Transmission State** (in `sender.py`)

- Fields:
  - `seq_num` (uint32): Sequence number of the next packet to send
  - `base` (uint32): Sequence number of the oldest unacknowledged packet
  - `cwnd` (int): Congestion window size (in packets)
  - `ssthresh` (int): Slow start threshold
  - `rwnd` (int): Receiver advertised window
  - `packet_buffer` (list): Buffer storing transmitted but unacknowledged packets
  - `dup_ack_count` (int): Counter for duplicate ACK detection
  - `file_data` (bytes): Contents of the input file
  - `total_packets` (int): Total number of DATA packets to send
  - `timeout` (float): Sender timeout duration in seconds

- Invariants:
  - Sender transmission window is limited by `send_window = min(cwnd, rwnd)`
  - Packets may be transmitted while `nseq_num < base + send_window`
  - On 3 duplicate ACKs, fast retransmit is triggered
  - On timeout, `ssthresh` is updated and `cwnd` resets to 1

**Receiver Reception State** (in `receiver.py`)

- Fields:
  - `expected_seq` (uint32): Sequence number expected
  - `rwnd` (int): Receiver available buffer space
  - `last_ack` (bytes): Most recently sent valid ACK packet
  - `received_packets` (list): Storage for received payload data
  - `total_packets` (int): Expected total number of packets (from first received packet)
  - `received_count` (int): Number of packets successfully received
  - `connection_state` (enum): Receiver connection state (LISTEN / ESTABLISHED / CLOSED)

- Invariants:
  - Receiver delivers DATA only if packet is valid/non-corrupt and `seq == expected_seq`
  - Duplicate or corrupt DATA packets are not delivered
  - Receiver sends cumulative ACKs indicating the highest in-order packet received
  - Receiver advertises `rwnd` in every ACK packet
  - Transfer completed when `received_count == total_packets`
  - Receiver participates in connection teardown after receiving FIN

### 5.2 Module Map and Dependencies

```
src/
|-- sender.py          # Phase 5(a–d): TCP-style sender
|-- receiver.py        # Phase 5(c–e): TCP-style receiver 
|-- packet.py          # Packet creation, parsing, and checksum utilities
|-- channel.py         # Bit-error and packet loss injection simulation (Options 1-5)
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

**Phase 5(a-e) - TCP-Style Sender Behavior**

Steps:
1. Open BMP file
2. Read the file and split into fixed-size chunks (<= 1024 bytes)
3. Initialize sender variables:
	a. `seq_num = 0`
	b. `base = 0`
	c. `cwnd = 1`
	d. `ssthresh = initial_threshold`
	e. `rwnd = receiver_advertised_window`
	f. `dup_ack_count = 0`
4. Begin connection establishment using a simplified three-way handshake:
	a. Send `SYN`
	b. Wait for `SYN-ACK`
	c. Reply with `ACK`
5. After the connection is established, begin data transfer.
6. Compute the effective sender window `send_window = min(cwnd, rwnd)`
7. While packets remain to be sent:
	a. If `seq_num < base + send_window`, create and send a DATA packet
   	b. If `base == seq_num`, start the retransmission timer
   	c. Increment `seq_num`
8. Upon receiving ACK
   	a. Validate checksum
   	b. f the ACK is new, slide the window forward by updating `base`
   	c. Reset `dup_ack_count` if needed
9. If a duplicate ACK is received:
	a. Increment `dup_ack_count`
	b. If `dup_ack_count == 3`, perform fast retransmit:
		i. Retransmit the missing packet immediately
		ii. set `ssthresh = cwnd / 2`
		iii. set `cwnd = ssthresh + 3`
10. If a timeout occurs:
	a. a. Retransmit the oldest unacknowledged packet
	b. Set `ssthresh = cwnd / 2`
	c. Set `cwnd = 1`
	d. Restart slow start
	e. Restart the timer
11. Continue until all packets are acknowledged
12. After file transfer completes, begin connection teardown:
	a. Send `FIN`
	b. Wait for `ACK`
	c. Wait for receiver `FIN`
	d. Send final `ACK`

**Phase 5(a-e) Sender Pseudocode:**

```
initialize seq_num = 0
initialize base = 0
initialize cwnd = 1
initialize ssthresh = initial_threshold
initialize dup_ack_count = 0

send SYN
wait for SYN-ACK
send ACK

while base < total_packets do

    send_window = min(cwnd, rwnd)

    if seq_num < base + send_window then
        send packet[seq_num]

        if base == seq_num then
            start timer
        end if

        seq_num += 1
    end if

    if new ACK received then
        base = ACK + 1
        dup_ack_count = 0

        if cwnd < ssthresh then
            cwnd = cwnd + 1
        else
            cwnd = cwnd + (1 / cwnd)
        end if

        if base == seq_num then
            stop timer
        else
            restart timer
        end if
    end if

    if duplicate ACK received then
        dup_ack_count += 1

        if dup_ack_count == 3 then
            ssthresh = cwnd / 2
            cwnd = ssthresh + 3
            retransmit missing packet
        end if
    end if

    if timeout then
        ssthresh = cwnd / 2
        cwnd = 1
        retransmit packet[base]
        restart timer
    end if

end while

send FIN
wait for ACK
wait for FIN
send ACK
```

### 6.2 Receiver Behavior

**Phase 5(c-e) - TCP-Style Receiver Behavior**

Steps:
1. Bind UDP socket to receiver port
2. Initialize receiver variables:
	a. `expected_seq = 0`
	b. `received_count = 0`
	c. `rwnd = receiver_buffer_size`
	d. `connection_state = LISTEN`
3. Wait for connection establishment:
	a. Receive `SYN` from sender
	b. Reply with `SYN-ACK`
	c. Wait for final `ACK`
	d. Transition to `ESTABLISHED`
4. Loop until all packets are received.
5. When a DATA packet arrives:
	a. Validate checksum
	b. Check whether `seq == expected_seq`
6. If the packet is valid and in order:
	a. Deliver payload
	b. Store payload
	c. Update `received_count`
	d. Increment `expected_seq`
7. If the packet is corrupt or out of order:
	a. Discard packet
	b. Send the last valid cumulative `ACK`
8, Continue receiving packets until the full file has been reconstructed.
9. Reassemble the file and write it to disk.
10. Wait for connection teardown:
	a. Receive `FIN` from sender
	b. Reply with `ACK`
	c. Send `FIN`
	d. Wait for final `ACK`
	e. Transition to `CLOSED`
	
**Phase 5(c-e) Pseudocode:**

```
initialize expected_seq = 0
initialize received_count = 0
initialize rwnd = receiver_buffer_size
initialize last_ack = ACK(-1)
initialize connection_state = LISTEN

wait for SYN
send SYN-ACK
wait for ACK
connection_state = ESTABLISHED

while received_count < total_packets do

    receive packet

    if packet corrupt OR packet.seq != expected_seq then
        send last_ack

    else
        deliver payload
        store payload
        received_count += 1
        expected_seq += 1
        update rwnd
        last_ack = make_ACK(expected_seq - 1, rwnd)
        send last_ack
    end if

end while

reassemble file and write to disk

wait for FIN
send ACK
send FIN
wait for final ACK
connection_state = CLOSED
```

### 6.3 Error / Loss Injection Specification

During Phase 5 testing:
- Option 1: Normal Transfer
	- No packet corruption or loss occurs.
	- Used to demonstrate successful connection establishment, data transfer, and connection teardown.
- Option 2: Flow-Control-Limited Transfer
	- Receiver advertises a small receive window `(rwnd)`.
	- Sender transmission rate is limited by the receiver buffer size.
- Option 3: Slow Start Behavior
	- No packet loss is introduced.
	- Congestion window `(cwnd)` grows exponentially during slow start and transitions into congestion avoidance.
- Option 4: Duplicate ACK Scenario (Fast Retransmit)
	- Duplicate ACKs are generated to simulate packet loss detection without timeout.
	- Sender detects three duplicate ACKs and performs fast retransmit and fast recovery.
- Option 5: Timeout-Based Loss Detection
	- A DATA packet is intentionally dropped during transmission.
	- Sender fails to receive an ACK before timeout.
	- Sender retransmits the missing packet and resets congestion control parameters.

---

## 7 Experiments and Metrics Plan

Phase 5 evaluates the behavior of the TCP-style transport protocol, including congestion control and flow control mechanisms, under various network conditions.

The same BMP file is transferred under 5 scenarios: 
- Option 1: Normal TCP transfer (no loss or corruption)
- Option 2: Flow-control-limited transfer (restricted receiver window `rwnd`)
- Option 3: Slow start behavior
- Option 4: Reno fast retransmit / fast recovery (duplicate ACK scenario)
- Option 5: Timeout-based congestion response (packet loss causing retransmission)

### 7.1 Setup

- Payload size: 1024 bytes
- Transport protocol: TCP-style reliable transfer over UDP
- Congestion control mechanisms:
	- Slow start
	- Congestion avoidance
	- Fast retransmit
	- Fast recovery
- Flow control: receiver-advertised window `(rwnd)`
- Checksum: CRC32
- Packet loss/error rates: experiments run across loss rates from 0% to 95% in increments of 5%

Each rate is tested:
- 5 independent runs
- Same input BMP file
- Debug logging disabled during timing

### 7.2 Timing Measurement 

End-to-end completion time is measured at the sender and includes:
	- Retransmissions due to packet loss
	- Congestion window adjustments
	- Flow control limitations
	- Duplicate ACK handling
	- Timeout recovery events
	
Timing begins when the first packet is transmitted and ends when the final packet is acknowledged and the transfer completes.

### 7.3 Plot Generation 

Two plots are generated:

Plot 1: Completion Time vs Packet Loss
- X-axis: error rate (%)
- Y-axis: average completion time (seconds)
- Five lines representing Options 1–5
- Completion time is expected to increase as packet loss rises due to retransmissions and congestion control adjustments.

Plot 2: Congestion Window Evolution
- X-axis: transmission rounds (or time)
- Y-axis: congestion window size `(cwnd)`
- The graph will illustrate:
	- Exponential growth during slow start
	- Linear growth during congestion avoidance
	- Reductions caused by fast retransmit or timeouts

### 7.4 Correctness Validation
For every run:
- The output file must match the input file byte-for-byte.
- Sequence numbers must alternate correctly.
- Congestion control transitions must follow expected TCP behavior.
- No deadlocks, infinite retransmissions, or stalled connections may occur.
- The connection must terminate successfully after file transfer.

**Output Artifacts:**
- TBD

---

## 8 Edge Cases and Test Plan

Phase 5 validates the TCP-style transport protocol, including connection management, congestion control, flow control, and loss recovery.

### 8.1 Expected Edge Cases

| Edge case | Why it matters | Expected behavior |
|---|---|---|
| Last packet smaller than payload size | Correct file reconstruction | Receiver writes exact bytes |
| Corrupted DATA packet | Receiver must detect via checksum | Receiver discards packet and sends last valid ACK |
| Corrupted ACK packet | Sender must detect corruption | Sender ignores ACK and retransmits after timeout |
| Duplicate DATA packet | Caused by retransmission | Receiver discards packet and resends last ACK |
| Out of order packet | Occurs with Go-Back-N pipeline | Receiver discards packet and sends last ACK | 
| Duplicate ACKs | Trigger fast retransmit | Sender detects 3 duplicate ACKs and retransmits missing packet| 
| High error rate (≥80%) | Stress test | Transfer completes eventually |
| Lost DATA packet | Receiver never receives packet | Sender times out and retransmits |
| Lost ACK packet | Sender never sees ACK | Sender times out and retransmits |
| SYN packet loss | Connection establishment robustness | Sender retransmits SYN | 
| FIN packet loss | Connection teardown reliability | Sender retransmits FIN until acknowledged | 

### 8.2 Tests
- `test_make_parse_roundtrip`: `make_packet(seq, payload, total)` then `parse_packet()` returns the same fields
- `test_max_payload_1024`: payload of exactly 1024 bytes encodes/decodes correctly
- `test_small_payload`: payloads of less than 1024 bytes encodes/decodes correctly
- `test_checksum_correct`: checksum function produces the expected value and detects corruption
- `test_ack_packet_format`: ACK packets are encoded/decoded correctly and contain only ACK fields.
- `test_data_packet_format`: DATA packets include expected fields and validate correctly.
- `test_control_packet_format`: SYN and FIN packets encode and decode correctly.
- `test_data_packet_format`: DATA packets include expected fields and validate correctly.

**Integration Tests:**

- Option 1: Normal Transfer
	- Establish connection using handshake
	- Transfer file successfully
	- Confirm byte-for-byte match
	- Confirm connection teardown completes
  
- Option 2: Flow-Control-Limited Transfer
	- Restrict receiver window `(rwnd)`
	- Confirm sender respects flow control limit
	- Confirm correct file reconstruction
  
- Option 3: Slow Start Behavior
	- Monitor congestion window `(cwnd)` growth
	- Confirm exponential growth during slow start
	- Confirm transition to congestion avoidance
  
- Option 4: Fast Retransmit / Fast Recovery
	- Trigger duplicate ACK scenario
	- Confirm sender detects 3 duplicate ACKs
	- Confirm immediate retransmission of missing packet
  
- Option 5: Timeout-Based Loss Recovery
	- Intentionally drop DATA packet
	- Confirm timeout occurs
	- Confirm retransmission and congestion window reset

### 8.3 Test Artifacts

- Console logs saved to `results/logs/`
- Output files from tests in `results/`
- Test scripts in `tests/`

### 8.4 FSM Validation

**Ensure sender states match Go-Back-N FSM behavior.**

- Sender states:
	- Connection establishment (SYN sent)
	- Data transmission (ESTABLISHED)
	- Congestion control adjustments
	- Loss recovery
	- Connection teardown (FIN sent)

- Receiver states:
	- LISTEN (waiting for SYN)
	- ESTABLISHED (receiving DATA)
	- Sending cumulative ACKs
	- Handling retransmissions
	- Connection teardown and CLOSED state

---

## 9 Repository Structure and Reproducibility
```
src/
  sender.py
  receiver.py
  packet.py
  channel.py

scripts/
  phase5_experiments.py

results/
  phase5_raw.csv
  phase5_avg.csv
  phase5_plot.gp
  phase5_plot.png

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
| Implement TCP-style connection setup (SYN / SYN-ACK / ACK) | Olivia Pham | 4/30/26 | Sender and receiver complete three-way handshake before data transfer |
| Implement TCP-style sender transmission logic | Olivia Pham | 4/30/26 | Sender maintains `seq_num`, `base`, and dynamic sender window |
| Implement congestion control (slow start and congestion avoidance) | Olivia Pham | 4/30/26 | `cwnd` grows correctly during slow start and transitions to congestion avoidance |
| Implement fast retransmit and fast recovery | Olivia Phan | 4/30/26 | Sender detects 3 duplicate ACKs and retransmits missing packet | 
| Implement TCP-style receiver logic and flow control | Olivia Pham | 4/30/26 | Receiver advertises `rwnd` and sends cumulative ACKs | 
| Implement DATA packet loss simulation | Cody Nguyen | 4/30/26 | Packet loss triggers retransmission and congestion response |
| Implement DATA bit-error injection | Cody Nguyen | 4/30/26 | DATA corruption detected and handled |
| Validate end-to-end correctness | Cody Nguyen | 4/8/26 | Output file matches original input file |
| Run performance experiments | Ian Khoo | 4/30/26 | Completion times collected |
| Generate performance plots | Ian Khoo | 4/30/26 | Graphs produced for analysis |

### 10.2 Milestones

1. TCP-style three-way handshake implemented (SYN / SYN-ACK / ACK)
2. Sender implements dynamic congestion window `(cwnd)` behavior
3. Receiver correctly implements flow control using advertised window `(rwnd)`
4. Slow start and congestion avoidance operate correctly during data transfer
5. Duplicate ACK detection triggers fast retransmit / fast recovery
6. Timeout-based retransmission correctly resets congestion window
7. End-to-end file transfer works under all five Phase 5 demo scenarios
8. Completion time and congestion window metrics collected across loss rates
9. Performance plots generated
10. Demo video(s) recorded

---

## 11 Demonstration Checklist

### Pre-Recording Checklist

**Phase 5 (Option 1):**
- [ ] Both terminal windows visible side-by-side
- [ ] Demonstrate connection establishment (SYN / SYN-ACK / ACK)
- [ ] Successful file transfer shown
- [ ] Demonstrate connection teardown (FIN / ACK)

**Phase 5 (Option 2):**
- [ ] Both terminal windows visible side-by-side
- [ ] Receiver advertises small rwnd
- [ ] Sender transmission rate visibly limited by receiver window

**Phase 5 (Option 3):**
- [ ] Both terminal windows visible side-by-side
- [ ] Show cwnd increasing during slow start
- [ ] Show transition into congestion avoidance

**Phase 5 (Option 4):**
- [ ] Both terminal windows visible side-by-side
- [ ] Show duplicate ACKs being generated
- [ ] Show fast retransmit triggered after 3 duplicate ACKs

**Phase 5 (Option 5):**
- [ ] Both terminal windows visible side-by-side
- [ ] DATA packet loss demonstration
- [ ] Show timeout-based retransmission and cwnd reset
      
**Video Quality:**
- [ ] Both terminal windows visible side-by-side
- [ ] Clear explanation of steps
- [ ] Show file comparison/verification


