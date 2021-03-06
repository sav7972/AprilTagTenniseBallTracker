#!/usr/bin/env python 

""" 
A simple echo server 
""" 

import socket 

host = '192.168.0.223'
port = 8081 
backlog = 5 
size = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port))
s.listen(backlog) 
while 1: 
    client, address = s.accept() 
    print("connection made")
    data = client.recv(size) 
    print(data)
    if data: 
        client.send(data)
    client.close()