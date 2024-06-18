import socket
import json
import os
HST = './socket4'
PORT = 1024
try:
    os.unlink(HST)
except OSError:
    if os.path.exists(HST):
        raise
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.bind(HST)
s.listen(1)
client, addr = s.accept()
sub1 = dict()
sub1['numberOfTests'] = 10
sub1['id'] = 1
sub1['code'] = "#include<bits/stdc++.h>\n\
using namespace std;\
int dp[10003], p[10003], c[10003], d[10003];\
int main()\
{\
int n, T;\
cin >> n >> T;\
for(int i = 0; i < n; i++)\
    cin >> d[i];\
for(int i = 0; i < n; i++)\
    cin >> c[i];\
}"
sub2 = dict()
sub2['numberOfTests'] = 5
sub2['id'] = 2
sub2['code'] = "#include<bits/stdc++.h>\n\
using namespace std;\
int dp[10003], p[10003], c[10003], d[10003];\
int main()\
{\
int n, T;\
cin >> n >> T;\
for(int i = 0; i < n; i++)\
    cin >> d[i];\
for(int i = 0; i < n; i++)\
    cin >> c[i];\
}"
client.sendall(json.dumps(sub1).encode())
#client.sendall(json.dumps(sub2).encode())
while True:
	pass
client.close()
