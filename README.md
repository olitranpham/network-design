# Network Design Project – Don't Be COI

## Overview

## Team
| Name | Email | Primary responsibility |
|---|---|------------------------|
| Cody Nguyen | cody_nguyen@student.uml.edu | Phase 3(b)             | 
| Olivia Pham | olivia_pham@student.uml.edu | Phase 3(a)             |
| Ian Khoo | ian_khoo@student.uml.edu | Phase 3(c)             |


## Demo Video

- **Private YouTube link **
	- Link: https://youtu.be/vRdP3Vdgl78
		- Timestamped outline:
			- Phase 2(a)/Phase 2(b) Option 1 ==> 0:00 - 0:23
     		- Phase 2(b) Option 2 ==> 0:23 - 0:58
     		- Phase 2(b) Option 3 ==> 0:58 - 1:30
     		- Phase 2(c/d) Plot ==> 1:30 - 1:49


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
  phase3_experiments.py

results/
  phase3_avg.csv
  phase3_raw.csv
  phase3_plot.png

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
`python3 src/sender.py \
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
- (--data-biterr) probability of DATA corruption (Option 3)

### Receiver 
`python3 src/receiver.py \
  --port 9000 \
  --out results/out.bmp \
  --data-biterr <prob>`

flags:
- (--port) listen port
- (--out) output file
- (--data-biterr) DATA corruption probability (option 3)

### Injection Flags

- --ack-biterr: probability of ACK corruption (Option 2)
- --data-biterr: probability of DATA corruption (Option 3)

### Timing / Windowing Flags



---

## Quick Start (Run Locally)

Start receiver first, then run sender with desired flags.
---

## Required Demo Scenarios

### option 1 - RDT 3.0 File Transfer 

Server:
```
python3 src/receiver.py --port 9000 --out results/out.bmp --data-biterr 0.0

```

Client:
```
python3 src/sender.py --host 127.0.0.1 --port 9000 --file test-files/sample1.bmp --ack-biterr 0.0

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
python3 src/receiver.py --port 9000 --out results/out.bmp --data-biterr 0.0
```

Sender:
```
python3 src/sender.py --host 127.0.0.1 --port 9000 --file test-files/sample1.bmp --ack-biterr 0.2
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
python3 src/receiver.py --port 9000 --out results/out.bmp --data-biterr 0.2
```

Sender:
```
python3 src/sender.py --host 127.0.0.1 --port 9000 --file test-files/sample1.bmp --ack-biterr 0.0
```

File verification:
```
cmp test-files/sample1.bmp results/received.bmp && echo "MATCH"
```

Expected behavior:
- Receiver rejects corrupt packets 
- Duplicate ACKs 
- Sender retransmits

### option 4: ACK packet loss

Receiver:
```
python3 src/receiver.py --port 9000 --out results/out.bmp --data-loss 0.0
```

Sender:
```
python3 src/sender.py --host 127.0.0.1 --port 9000 --file test-files/sample1.bmp --ack-loss 0.2
```


Expected behavior:
- ACK packets are dropped
- Sender times out
- Sender retransmits last DATA packet
- File still correct

---

### option 5: DATA packet loss

Receiver:
```
python3 src/receiver.py --port 9000 --out results/out.bmp --data-loss 0.2
```


Sender:
```
python3 src/sender.py --host 127.0.0.1 --port 9000 --file test-files/sample1.bmp --ack-loss 0.0
```

Expected behavior:
- DATA packets are dropped
- Sender times out
- Sender retransmits
- File still correct

### Phase 3(c): Performance Evaluation
Run:
```
python3 scripts/phase3_experiments.py \
  --file test-files/bmp_24.bmp \
  --runs 5 \
  --max-attempts 60 \
  --timeout 0.005 \
  --hard-timeout 60 \
  --plot
  ```


## Figures / Plots
results/phase3_plot.png

### Results files
- 
results/phase3_raw.csv
results/phase3_avg.csv
results/phase3_plot.png
---

## Known Issues / Limitations
The program that runs the incremental tests for error percentage notably runs faster on machines with higher technical specifications.


---

## Academic Integrity / External Tools
Debugging tools (IDE debugger, logging) and LLMs may be used for learning and troubleshooting. Final implementation decisions and understanding are our own.

