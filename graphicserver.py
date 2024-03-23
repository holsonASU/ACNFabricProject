import socket

#connect to logic node
logicSocket = socket.socket()
logicPort = 12344
logicSocket.connect(('localhost', logicPort))
print("Graphics connected to Logic.")

#listen for client node
s = socket.socket()
port = 12343

s.bind(('', port))
s.listen(5)
c, addr = s.accept()
print("Graphics Connected to client.")

done = False

while done == False:
    message = logicSocket.recv(1024).decode()
    
    print(message)
    
    if "quit" in message.lower():
        done = True
    
    #render scene
    
    c.send(message.encode())

logicSocket.close()
s.close()