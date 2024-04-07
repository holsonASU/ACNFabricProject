import socket
import threading
from queue import Queue
import time
import random
import datetime

queue = Queue()

def clientConnection(c):
    
    global queue
    
    exit = False
    
    while exit == False:
        
        x = c.recv(1024).decode()
        out = "Logic received from client: " + x
        print(out)
        
        queue.put(x)
        logCommandReceived(x.split('@')[0])
        
        if "quit" in x.lower():
            exit = True
    
    print("LOGIC Shutting down client connection.")


def graphicsConnection(c):
    
    global queue
    
    exit = False
    
    while exit == False:
        commandList = []
        #process queue
        while queue.empty() == False:
            commandList.append(queue.get())
        
        message = "Message: "
        commandIndices = list()
        for command in commandList:
            
            lis = command.split('@')
            commandIndices.append(lis[0])
            
            if "quit" in command.lower():
                exit = True
                break
        
        
        message = str(commandIndices) + "@" + generateGraphicsMessage()
        print("Logic Message to Graphics: " + message)
        c.send(message.encode())
        
        if exit == True:
            print("Sending quit command")
            time.sleep(.4)
            c.send("quit")
            break
        
        cpuTime = random.gauss(4.70, 0.66) / 1000
        time.sleep(cpuTime)
    
    print("LOGIC Shutting down graphics connection.")

def generateGraphicsMessage():
    coords = ''
    for i in range(1000):
        coords = str(random.triangular(-10,10)) + ','
    return coords

def logCommandReceived(commandIndex):
    fileName = "logs/logicLog.txt"
    f = open(fileName, 'a')
    line = commandIndex + '|' + str(datetime.datetime.now()) + '\n'
    f.write(line)

if __name__ == "__main__":
    
    graphicIP = 'localhost'
    
    #connect to graphics
    print('LOGIC Waiting for Graphics Server...')
    graphicsSocket = socket.socket()
    port = 12344
    graphicsSocket.bind(('', port))
    graphicsSocket.listen(5)
    g, addrG = graphicsSocket.accept()
    print('LOGIC Got Graphics connection from', addrG)
    
    #connect to client
    print("LOGIC Waiting for CLient...")
    clientSocket = socket.socket()
    clientPort = 12345
    clientSocket.bind(('', clientPort))
    clientSocket.listen(5)
    c, addrC = clientSocket.accept()
    print('LOGIC Got Client connection from', addrC)
    
    t1 = threading.Thread(target=clientConnection, args=(c,))
    t2 = threading.Thread(target=graphicsConnection, args=(g,))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    c.close()
    g.close()
    graphicsSocket.close()
    clientSocket.close()
    
    print("LOGIC Done with both threads.")



