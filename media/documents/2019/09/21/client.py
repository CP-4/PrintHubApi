# Import socket module
import socket

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 8070

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# receive data from the server
rec = s.recv(1024)
# print(rec)
if rec == b'connected':
    with open('audio.wav', 'rb') as f:
        for l in f: s.sendall(l)

# close the connection
s.close()
