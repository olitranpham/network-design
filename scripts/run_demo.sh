## Phase 1(a) - UDP Echo

Terminal 1 (server):
`python server.py`

Terminal 2 (client):
`python client.py`

## Phase 1(b) - RDT 1.0 File Transfer

Terminal 1 (server):
`python receiver.py --port 9000 --output received.bmp`

Terminal 2 (client):
`python sender.py --host 127.0.0.1 --port 9000 --file test_files/test.bmp`
