import temp_pb2
import socket
import time
import sys

HOST = '127.0.0.1'
PORT = 8888
s = None

temp = temp_pb2.TempEvent()

for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.connect(sa)
    except OSError as msg:
        s.close()
        s = None
        continue
    break

if s is None:
    print("Couldn't connect to server")
    sys.exit(1)

with s:
    while True:
        temp.device_id = 1
        temp.event_id = 2
        temp.humidity = 3
        temp.video_data = 4
        s.sendall(temp.SerializeToString())
        print(f"send:\n{temp}")
        time.sleep(1)    
