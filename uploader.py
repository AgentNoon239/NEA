import socket
import sys

HAMACHI_IP = "25.32.32.32"
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HAMACHI_IP,PORT))

name = sys.argv[1].encode("utf-8")
s.send(int.to_bytes(len(name),1,"big"))
s.send(name)

with open(name,"rb") as f:
	d = f.read()

s.send(int.to_bytes(len(d),4,"little"))
s.send(d)