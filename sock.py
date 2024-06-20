import socket

# Sending string to socket using client
def send(string, client):
	send = string.encode()
	cnt = len(send)
	# Send number of bytes to write
	client.sendall(cnt.to_bytes(4, byteorder='big'))
	# Send the string itself
	client.sendall(send)

# Recieving string from socket using client
def recv(client):
	# Recieving number of bytes to read
	cnt = int.from_bytes(client.recv(4), byteorder='big')
	# Recieving the string itself
	response = client.recv(cnt)
	j = response.decode()
	return j
