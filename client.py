import socket
import threading
import sys
import time
import cv2
import datetime

done = False

def logicServerHandler(s, commandList):
    
    commandIndex = 0
    global done
    
    for command in commandList:
        message = str(commandIndex) + '@' + str(command[0])
        
        writeOutputToFile(commandIndex, False)
        
        print("CLIENTSENT: " + message)
        waitTime = float(command[1])
        s.send(message.encode())
        time.sleep(waitTime)
        commandIndex = commandIndex + 1
    
    time.sleep(.4)
    sys.exit()
    

def graphicsServerHandler(s):
    
    global done
    
    while done == False:
        
        index = s.recv(1024).decode()
        
        if 'quit' in index:
            break
        
        #fileSize = int(s.recv(1024).decode())
        
        #packets = fileSize/2048
        
        #framePacket = ''
        
        count = 0
        #while count < packets+1:
        #    framePacket = s.recv(2048)
        #    try:
        #        framePacket = framePacket.decode()
        #    except:
        #        framePacket = ''
        #    count = count + 1
       # 
        if index != '':
            writeOutputToFile(index, True)
        
        print("CLIENT RECEIVED: " + str(index))
    
    
def writeOutputToFile(index, received):
    f = open("logs/clientOutput.txt", 'a')
    line = ''
    if (received):
        line = "r:" +  str(index) + '|' + str(datetime.datetime.now()) + '\n'
    else:
        line = "s:" + str(index) + '|' + str(datetime.datetime.now()) + '\n'
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
    
    commandListFile = "clientCommands2.txt"
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