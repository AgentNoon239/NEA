import socket 

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serversocket.bind((socket.gethostname(), 8000))
# become a server socket
serversocket.listen(5)

while True:
	# accept connections from outside
	(clientsocket, address) = serversocket.accept()
	print("connection")
	# now do something with the clientsocket
	# in this case, we'll pretend this is a threaded server
	name_length = clientsocket.recv(1)
	name = clientsocket.recv(int.from_bytes(name_length,"big")).decode()
	file_length = int.from_bytes(clientsocket.recv(4),"little")
	
	print(file_length)

	with open("files/"+name.replace(":","_"),"wb") as f:
		recieved = 0
		while recieved < file_length:
			d = clientsocket.recv(min(file_length-recieved,1024))
			f.write(d)
			recieved += 1024

	print("Done")