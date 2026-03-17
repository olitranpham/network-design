## Phase 3 - RDT 3.0 File Transfer

Terminal 1 (receiver):
`python receiver.py --port 9000 --out received_output.txt`

Terminal 2 (sender):
`python sender.py --host 127.0.0.1 --port 9000 --file test.txt`
