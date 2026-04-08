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
	- Link: (https://youtu.be/G_qu06qyzf8)
		- Timestamped outline:
			- Phase 4 Option 1 ==> 0:00 - 0:20
     		- Phase 4 Option 2 ==> 0:20 - 0:53
     		- Phase 4 Option 3 ==> 0:53 - 3:03
     		- Phase 4 Option 4 ==> 3:03 - 3:35
       		- Phase 4 Option 5 ==> 3:35 - 5:52
         - Misclick of incorrect graph ==> 6:02 - 6:10
            - Phase 4 Generated Plots ==> 6:10 - 6:57


---

## Repository Structure 


project/
src/
  sender.py
  receiver.py
  packet.py
  channel.py

scripts/
  phase3_experiments.py
  phase4_experiments.py
  phase4_chart2.py
  phase4_chart3.py

results/
  phase3_avg.csv
  phase3_raw.csv
  phase3_plot.png
  phase4_chart1.png
  phase4_chart2.png
  phase4_chart3.png

test-files/
  sample1.bmp
  bmp_24.bmp


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
- --ack-loss: probability of ACK loss (Option 4)
- --data-loss: probability of DATA loss (Option 5)

### Timing / Windowing Flags



---

## Quick Start (Run Locally)

Run full experiment (Chart 1):

```bash
python3 scripts/phase4_experiments.py \
  --file test-files/bmp_24.bmp \
  --runs 5 \
  --max-attempts 10 \
  --window 4 \
  --timeout 0.2 \
  --hard-timeout 20 \
  --plot
```
## Required Demo Scenarios

### option 1 - Regular file trasnfer (no ERROR)

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

### ```md
## Phase 4: Go-Back-N (GBN)
Run:
```
python3 scripts/phase4_experiments.py \
  --file test-files/bmp_24.bmp \
  --runs 5 \
  --max-attempts 10 \
  --window 4 \
  --timeout 0.2 \
  --hard-timeout 20 \
  --plot
```

Chart 2: Window Size Evaluation
Run:
bash
```
python3 scripts/phase4_chart2.py
```
Chart 3: Phase Comparison
Run:

bash
```
python3 scripts/phase4_chart3.py
```
Key features:
- Sliding window at sender (window size N)
- Cumulative ACKs
- Timeout-based retransmission of entire window
- Supports error/loss injection for testing

Options tested:
1. No loss/errors
2. ACK bit errors
3. DATA bit errors
4. ACK loss
5. DATA loss

## Figures / Plots

### Chart 1: Phase 4 Performance
- X-axis: Loss/Error Rate (0%–95%)
- Y-axis: Completion Time
- Includes all 5 options

### Chart 2: Window Size vs Completion Time (10% Error)
- X-axis: Window Size (1, 2, 5, 10, 20, 50)
- Y-axis: Completion Time

### Chart 3: Phase Comparison
- X-axis: Phase 1–4
- Y-axis: Completion Time

### Files:
- results/phase4_chart1.png
- results/phase4_chart2.png
- results/phase4_chart3.png
- results/phase3_plot.png

## Known Issues / Limitations
The program that runs the incremental tests for error percentage notably runs faster on machines with higher technical specifications.


---

## Academic Integrity / External Tools
Debugging tools (IDE debugger, logging) and LLMs may be used for learning and troubleshooting. Final implementation decisions and understanding are our own.

