import socket
import threading
import sys
import time

def logicServerHandler(s, commandList):
    
    for command in commandList:
        message = str(command[0])
        print("CLIENTSENT: " + message)
        waitTime = float(command[1])
        s.send(message.encode())
        if message == "quit":
            break
        time.sleep(waitTime)
    
    
def graphicsServerHandler(s):
    
    done = False
    
    while done == False:
        
        message = s.recv(1024).decode()
        
        out = "From Graphics: " + message
        print("CLIENT RECEIVED: " + message)
        writeOutputToFile(out)
        
        if "quit" in message.lower():
            break
    
    
def writeOutputToFile(line):
    f = open("clientOutput.txt", 'a')
    f.write(line)
    f.close()

def readCommandList(filename):
    commandList = list()
    f = open(filename, "r")
    
    for line in f:
        split = line.split('|')
        waitTime = split[1]
        commands = split[0]
        commandList.append([commands, waitTime])
    return commandList
    


if __name__ == "__main__":
    
    commandListFile = "clientCommands.txt"
    logicIP = "localhost"
    graphicIP = "localhost"
    
    if len(sys.argv) > 1:
        commandListFile = sys.argv[1] 
        logicIP = sys.argv[2] 
        graphicIP = sys.argv[3]
    
    commandList = readCommandList(commandListFile)
    
    logicSocket = socket.socket()
    port = 12345
    logicSocket.connect((logicIP, port))
    
    graphicsSocket = socket.socket()
    port = 12343
    graphicsSocket.connect((graphicIP, port))
    
    t1 = threading.Thread(target=logicServerHandler, args=(logicSocket,commandList,))
    t2 = threading.Thread(target=graphicsServerHandler, args=(graphicsSocket,))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    logicSocket.close()
    graphicsSocket.close()
    
    print("Client Done with both threads.")