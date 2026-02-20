# Network Design Project – Don't Be COI

## Overview

## Team
| Name | Email | Primary responsibility |
|---|---|---|
| Cody Nguyen | cody_nguyen@student.uml.edu | Phase 2(b) | 
| Olivia Pham | olivia_pham@student.uml.edu | Phase 2(a) |
| Ian Khoo | ian_khoo@student.uml.edu | Phase 2(c)


## Demo Video

- **Private YouTube link - Phase 2(a)** 
	- Link: 
		- Timestamped outline:
			- 

- **Private YouTube link - Phase 2(b)** 
	- Link: 
		- Timestamped outline:
			- 

---

## Repository Structure 

```
project/
src/
  sender.py
  receiver.py
  packet.py
  channel.py

scripts/
  phase2d_experiments.py

results/
  phase2d_avg.csv
  phase2d_raw.csv
  phase2d_plot.png

test-files/
  sample1.bmp
```

## Requirements
- Language/runtime: Python 3.14.2
- OS tested: Windows
- Dependencies:
  - Python: `pip install -r requirements.txt`
  - gnuplot: `sudo apt-get install gnuplot`

---

## Standard CLI Interface 

### Sender
`python src/sender.py \
  --host 127.0.0.1 \
  --port 9000 \
  --file test-files/sample1.bmp \
  --timeout 0.2 \
  --ack-biterr <prob>`

flags:
- (--host) receiver address
- (--port) receiver port)
- (--file) input file
- (--timeout) retransmission timeout
- (--ack-biterr) ACK corruption probability (option 2)

### Receiver 
`python src/receiver.py \
  --port 9000 \
  --out results/out.bmp \
  --data-biterr <prob>`

flags:
- (--port) listen port
- (--out) output file
- (--data-biterr) DATA corruption probability (option 3)

### Injection Flags


### Timing / Windowing Flags



---

## Quick Start (Run Locally)

Run receiver in one terminal and sender in another using the commands below.

---

## Required Demo Scenarios

### option 1 - RDT 2.2 File Transfer 

Server:
```
python src/receiver.py --port 9000 --out results/out.bmp --data-biterr 0.0

```

Client:
```
python src/sender.py --host 127.0.0.1 --port 9000 --file test-files/sample1.bmp --ack-biterr 0.0

```

File verification:
```
cmp test-files/sample1.bmp results/received.bmp && echo "MATCH"
```

Expected behavior:
- No retransmissions 
- File matches exactly

### option 2: ACK bit errors

Receiver:
```
python src/receiver.py --port 9000 --out results/out.bmp --data-biterr 0.0
```

Sender:
```
python src/sender.py --host 127.0.0.1 --port 9000 --file test-files/sample1.bmp --ack-biterr 0.2
```

File verification:
```
cmp test-files/sample1.bmp results/received.bmp && echo "MATCH"
```

Expected behavior:
- Corrupt ACK detected 
- Retransmissions occur 
- File still correct

### option 3: DATA bit errors

Receiver:
```
python src/receiver.py --port 9000 --out results/out.bmp --data-biterr 0.2
```

Sender:
```
python src/sender.py --host 127.0.0.1 --port 9000 --file test-files/sample1.bmp --ack-biterr 0.0
```

File verification:
```
cmp test-files/sample1.bmp results/received.bmp && echo "MATCH"
```

Expected behavior:
- Receiver rejects corrupt packets 
- Duplicate ACKs 
- Sender retransmits

### Phase 2(d): Performance Evaluation
Run:
```
python3 -u scripts/phase2d_experiments.py \
  --file test-files/sample1.bmp \
  --runs 5 \
  --timeout 0.2 \
  --hard-timeout 15 \
  --max-attempts 30 \
  --plot
  ```


## Figures / Plots

### Results files
- 
results/phase2d_raw.csv
results/phase2d_avg.csv
results/phase2d_plot.png
---

## Known Issues / Limitations



---

## Academic Integrity / External Tools
Debugging tools (IDE debugger, logging) and LLMs may be used for learning and troubleshooting. Final implementation decisions and understanding are our own.

