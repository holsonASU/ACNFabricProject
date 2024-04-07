import socket
import sys
import random
import time

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
        print("Quit has been received.")
        done = True
        c.send("quit")
    
    #render scene
    
    renderTime = random.gauss(8.33, 0.32) / 1000
    time.sleep(renderTime)
    
    c.send(message.encode())

logicSocket.close()
s.close()
print("Graphics Exited Gracefully.")