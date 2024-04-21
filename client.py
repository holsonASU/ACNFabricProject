import socket
import threading
import sys
import time
import datetime
from mlsocket import MLSocket

done = False

def logicServerHandler(s, commandList):
    
    commandIndex = 0
    global done
    
    for command in commandList:
        try:
            message = str(commandIndex) + '@' + str(command[0])
            
            #writeOutputToFile(commandIndex, False)
            line = "s@" + str(commandIndex) + '|' + str(datetime.datetime.now())
            
            print(line)
            waitTime = float(command[1])
            s.send(message.encode())
            time.sleep(waitTime)
            commandIndex = commandIndex + 1
        except:
            break
    
    time.sleep(.4)
    sys.exit()
    

def graphicsServerHandler(s):
    
    global done
    
    while done == False:
        try:
             index = s.recv(1024).decode()
             image = s.recv(1024)
             
             if 'quit' in index:
                 break

             
             count = 0
             
             line = "r@" +  str(index) + '|' + str(datetime.datetime.now())
             print(line)
           
            #if index != '':
                #writeOutputToFile(index, True)
        except:
            done = True
        
    
    
def writeOutputToFile(index, received):
    f = open("clientOutput.txt", 'a')
    line = ''
    if (received):
        line = "r@" +  str(index) + '|' + str(datetime.datetime.now()) + '\n'
    else:
        line = "s@" + str(index) + '|' + str(datetime.datetime.now()) + '\n'
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
    
    graphicsSocket = MLSocket()
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