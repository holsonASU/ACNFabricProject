import socket
import threading
from queue import Queue
import time

queue = Queue()

def clientConnection(c):
    
    global queue
    
    exit = False
    
    while exit == False:
        
        x = c.recv(1024).decode()
        out = "Logic received from client: " + x
        print(out)
        
        commands = x.split(',')
        
        for command in commands:
            queue.put(command)
        
        if "quit" in x.lower():
            exit = True
    
    print("LOGIC Shutting down client connection.")


def graphicsConnection(c):
    
    global queue
    
    exit = False
    
    commandList = []
    
    while exit == False:
        
        #process queue
        while queue.empty() == False:
            commandList.append(queue.get())
            
        
        message = "Message: "
        for command in commandList:
            message += " {}".format(command)
            if "quit" in command.lower():
                exit = True
                break
        
        commandList = []
        print(message)
        c.send(message.encode())
        
        if exit == True:
            break
        
        time.sleep(.3)
    
    print("LOGIC Shutting down graphics connection.")


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



