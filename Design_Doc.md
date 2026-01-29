# Network Design Project – Phase Proposal & Design Document (Phase 1 of 5)

> **Purpose:** This document is your team’s *proposal* for how you will implement the current phase **before** you start coding.  
> Keep it clear, concrete, and lightweight.

**Team Name:**  
**Members:** (Olivia Pham, olivia_pham@student.uml.edu)  
**GitHub Repo URL (with GitHub usernames):** https://github.com/olitranpham/network-design, olitranpham 
**Phase:** (1)  
**Submission Date:**  
**Version:** (v1)

---

## 0) Executive summary

For Phase 1 of this 5-phased project, UDP socket programming will be implemented with Python for a client and server, displaying bidirectional message transfer and an echo workflow. The first deliverable (Phase 1B) sends a "HELLO" message from the UDP client to the UDP server and echoes back to the client using different port numbers, although the client and server can run on the same machine. The second deliverable (Phase 1B) transfers a BMP image file from the client to server over UDP, while implementing the RDT 1.0 protocol. The sender will parse the BMP into fixed-size chunks and send one packet at a time, while the receiver reassembles packets in order and reconstructs the output BMP. Validation will be shown via a YouTube video plus a file-compare check. 

---

## 1) Phase requirements
### 1.1 Demo deliverable

- **Private YouTube link:** *(fill in at submission time)*  
  - Link: https://youtu.be/rH1DO7EJlp4
  - Timestamped outline (mm:ss → scenario name):
  	- 0:00-0:04 -> UDP server initialized and waiting for incoming message
    - 0:04-0:11 -> UDP client sends "HELLO" to server, server receives message and echoes back to client

### 1.2 Required demo scenarios
Fill in the scenarios required by the phase spec.

| Scenario | What you will inject / configure | Expected observable behavior | What we will see in the video |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |

### 1.3 Required figures / plots

N/A

---

## 2) Phase plan (company-style, lightweight)

### 2.1 Scope: what changes/additions this phase
- **New behaviors added:** 
	- UDP client sends "HELLO" message to server, server echoes message back to client
	- BMP file is transferred from client to server using RDT 1.0 behavior
	- Input file is parsed and packetized into fixed sizes using Make_Packet function
- **Behaviors unchanged from previous phase:** No prior behaviors since this is the initial phase
- **Out of scope (explicitly):**
	- No implementation to handle packet loss or corruption

### 2.2 Acceptance criteria (your checklist)

- [ ] Client/server run via CLI with configurable ports.
- [ ] "HELLO" is sent to client, sent and echoed to server, and sent back to client
- [ ] Select a BMP image file to transfer
- [ ] Packetize the BMP image file
- [ ] UDP sockets send and receive packets one file at a time
- [ ] Receiver assembles packets in order and writes a complete output file in order
- [ ] Receiver is delivered the entire transfer file
- [ ] README.md is complete
- [ ] Invite instructor(s) to GitHub repo and include GitHub link
- [ ] Record demo and upload to YouTube 

### 2.3 Work breakdown (high-level; myself)
- Workstream A: UDP socket used to send and receive packets + "HELLO" echo demo
- Workstream B: Make_Packet function + create sender/receiver file
- Workstream C: Compare input BMP file to output

---

## 3) Architecture + state diagrams

### 3.1 How to evolve the provided state diagram
For each phase:
1. **Start from the current phase diagram** (sender + receiver).
2. **Mark specifics**:
   - new states,
   - new transitions,
   - updated transition conditions (timeouts, corruption checks, window slide rules).
3. Keep both:
   - **“Previous phase diagram”** (for comparison) and
   - **“Current phase diagram”** (what you will implement in more detail).

> Tip: In your PDF submission, include diagrams as images. In Markdown, you can include ASCII diagrams or link to images in `docs/figures/`.

### 3.2 Component responsibilities
- **Sender**
  - Responsibilities:
	- Phase 1(a): Send "HELLO" and receive echo response
	- Phase 1(b): Open BMP file, packetize, and send one packet at a time
	- Send end packet for definite receiver termination 
- **Receiver**
  - Responsibilities:
	- Phase 1(a): Receive "HELLO" and echo back to sender
	- Phase 1(b): Receive packets and rewrite them in order, stop on end packet
- **Shared modules/utilities**
  - Packet encode/decode: Safely pack/unpack header and payload
  - Checksum: Not required for RDT 1.0 but can optionally be added for troubleshooting
  - Logging/timing: Mini progress logs (ex. bytes sent/received) 
  - CLI/config parsing: Host, ports, file path, chunk size

### 3.3 Message flow overview

Phase 1(a):
[client] --["HELLO"]-> [server]
[client] <-["HELLO"]-- [server]

Phase 1(b):
[input.bmp] -> sender -> UDP port -> receiver -> [output.bmp]
---

## 4) Packet format (high-level spec)

### 4.1 Packet types
List the packet types you will send:
- DATA: carries chunks of BMP file
- END: indicates end of file transfer


### 4.2 Header fields (this is the “field table”)

| Field | Size (bytes/bits) | Type | Description | Notes |
|---|---:|---|---|---|
| type | 1 byte | uint8 | 0 = DATA, 1 = END | Simple data parsing |
| seq | 4 bytes | uint32 | Packet sequence number | Starts at 0 and increments by 1 per DATA packet |
| ack |  |  | ack number / flag |  |
| len | 2 bytes | uint16 | Payload length in bytes | Last packet may be smaller than 1024 bytes |
| checksum |  |  | checksum value | what it covers (header/payload) |
| payload | ≤ ~1024B | bytes | file chunk | binary-safe |

---

## 5) Data structures + module map

### 5.1 Key data structures
1. Packet (encode/decode structure)
- Fields: type, seq, len, payload
- Invariants:
	- Type in {DATA, END}
	- If type == END, then len == 0 and payload == b''
	- If type == DATA then 0 < len <= 1024
- Location: src/packet.py

2. Sender state
- Fields: sock, server_addr, chunk_size=1024, next_seq, file_handle
- Invariants:
	- Sends DATA packets in increasing seq
	- Only one outstanding packet at a time
- Location: src/sender.py

3. Receiver state
- Fields: sock, expected_seq, out_file_handle
- Invariants:
	- Writes DATA payloads in order via expected_seq
- Location: src/receiver.py

### 5.2 Module map + dependencies
- src/packet.py
- src/sender.py
- src/receiver.py

Provide a simple dependency sketch:

sender     -> packet, utils
receiver   -> packet, utils

## 6) Protocol logic (high-level spec before implementation)

### 6.1 Sender behavior
- Phase 1(a):
	1. Create UDP socket
	2. Send "HELLO" to server
	3. Print received message
- Phase 1(b):
	1. Open input BMP in binary
	2. Loop
		- Read up to 1024 bytes
		- Create DATA packet with seq, len, and payload
		- Send packet over UDP
		- Increment seq
	3. Close file/socket
	
**Sender pseudocode (recommended):**
# Initialize UDP socket
seq = 0
while True: 
	chunk = read(file, 1024)
	if chunk is empty: break
	pkt = make_data_packet(type = DATA, seq = seq, len = len(chunk), payload = chunk)
	udp_send(pkt)
	seq += 1
udp_send(make_end_packet(type = END, seq = seq, len = 0))

### 6.2 Receiver behavior
- Phase 1(a):
	1. Bind UDP socket to server port
	2. Receive "HELLO" from sender
	3. Echo message back to sender address
- Phase 1(b):
	1. Bind UDP socket to server port
	2. Open output BMP
	3. Loop:
		- Receive UDP data
		- Parse header
		- If END: break
		- If DATA: Accept in sequential order
	4. Close file/socket

**Receiver pseudocode (recommended):**
expected_seq = 0
open output file
whilel True:
	pkt = udp_recv()
	parse(pkt)
	if type == END: break
	if type == DATA:
		write(payload)
		expected_seq += 1
close file

### 6.3 Error/loss injection spec (if required by phase)
If the phase requires injection, state:
- where injection occurs in the pipeline (exact point)
- probability model and RNG seed usage
- what is injected (bit flip vs drop)
- how you ensure repeatability

---

## 7) Experiments + metrics plan (required if phase requires figures/plots)
### 7.1 Measurement definition
Define completion time precisely:
- start moment:
- stop moment:

State how you will avoid measurement distortion:
- disable verbose printing/logging during timing runs
- run multiple trials if required

### 7.2 Output artifacts
- CSV schema (columns):
- plot filenames:
- where outputs are stored (`results/`):

---

## 8) Edge cases + test plan
This replaces “risks” with what actually matters for correctness.

### 8.1 Edge cases you expect
List the top edge cases you will explicitly test.

| Edge case | Why it matters | Expected behavior |
|---|---|---|
| last packet smaller than payload size | correct file reconstruction | receiver writes exact bytes |
| duplicate packets/ACKs | protocol correctness | ignored or re-ACKed |
| corrupted header | checksum coverage | drop / request retransmit |
| termination marker handling | clean shutdown | no deadlocks |

### 8.2 Tests you will write because of these edge cases
List concrete tests (unit/integration) that map to the edge cases.

- Unit tests:
	- Packet encode/decode with binary payloads
	- END packet parsing (len = 0, no payload)
- Integration tests (examples):
 	- Transfer small binary file
	- Transfer BMP and verify byte-for-byte with original file

### 8.3 Test artifacts
State what artifacts you will produce:
- console logs (minimal)
- where tests live (`tests/` optional, or `scripts/`)

---

## 9) Repo structure + reproducibility
Your repo must contain at minimum:

```
src/
scripts/
docs/
results/
README.md
```

State where phase artifacts live:
- Design docs: `docs/`
- Figures/plots + CSV: `results/`
- Any helper scripts: `scripts/`

---

## 10) Team plan, ownership, and milestones
### 10.1 Task ownership
| Task | Owner | Target date | Definition of done |
|---|---|---|---|
| Packet format + encode/decode | Self | 1/27/26 |  |
| Sender logic | Self | 1/27/26 |  |
| Receiver logic | Self | 1/28/26 |  |
| Injection (if required) |  |  |  |
| Figures/plots (if required) |  |  |  |
| README + reproducibility | Self | 1/30/26 |  |

### 10.2 Milestones (keep it realistic)
- Milestone 1:
- Milestone 2:
- Milestone 3:

---


## Appendix (optional)


