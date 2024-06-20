import socket
import json
import os
import sys
from sock import send, recv
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
sub1['judge'] = 0
sub1['verdict'] = 'NONE'
sub1['test'] = 0
sub1['maxTL'] = 'NONE'
sub1['maxML'] = 'NONE'
sub1['IOI'] = 'NONE'
sub1['checkerResult'] = 'NONE'
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
sub2['verdict'] = 'NONE'
sub2['checkerResult'] = 'NONE'
sub2['test'] = 0
sub2['maxTL'] = 'NONE'
sub2['maxML'] = 'NONE'
sub2['IOI'] = 'NONE'
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
tmp = json.loads(recv(client))
while tmp['type'] != "judge":
    print(tmp)
    tmp = json.loads(recv(client))
print(tmp)
sub1['judge'] = tmp['judge']
send(json.dumps(sub1), client)

tmp = json.loads(recv(client))
while tmp['type'] != "judge":
    print(tmp)
	tmp = json.loads(recv(client))
print(tmp)
sub2['judge'] = tmp['judge']
send(json.dumps(sub2), client)
while True:
	pass
client.close()
