import socket

def send(string, client):
	send = string.encode()
	cnt = len(send)
	client.sendall(cnt.to_bytes(4, byteorder='big'))
	client.sendall(send)
	
def recv(client):
	cnt = int.from_bytes(client.recv(4), byteorder='big')
	response = client.recv(cnt)
	j = response.decode()
	return j
