import socket
import threading

def logicServerHandler(s):
    
    done = False
    
    while done == False:
        message = input("What is the message?")
        
        s.send(message.encode())
        if message == "quit":
            done = True
    
    s.close()
    
def graphicsServerHandler(s):
    
    done = False
    
    while done == False:
        
        message = s.recv(1024).decode()
        
        out = "From Graphics: " + message
        writeOutputToFile(out)
        
        if message == "quit":
            break
    
    s.close()
    
def writeOutputToFile(line):
    f = open("clientOutput.txt", 'a')
    f.write(line)
    f.close()


if __name__ == "__main__":
    
    logicSocket = socket.socket()
    port = 12345
    logicSocket.connect(('localhost', port))
    
    graphicsSocket = socket.socket()
    port = 12343
    graphicsSocket.connect(('localhost', port))
    
    t1 = threading.Thread(target=logicServerHandler, args=(logicSocket,))
    t2 = threading.Thread(target=graphicsServerHandler, args=(graphicsSocket,))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print("Done with both threads.")