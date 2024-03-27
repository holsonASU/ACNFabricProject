import socket
import sys

logicIP = 'localhost'

if len(sys.argv) > 1:
    logicIP = sys.argv[1]

#connect to logic node
logicSocket = socket.socket()
logicPort = 12344
logicSocket.connect((logicIP, logicPort))
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
    
    print("GRAPHICS RECEIVED FROM LOGIC: " + message)
    
    if "quit" in message.lower():
        done = True
    
    #render scene
    
    c.send(message.encode())

logicSocket.close()
s.close()
print("Graphics Exited Gracefully.")