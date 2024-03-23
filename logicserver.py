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
        
        queue.put(x)
        
        if x == 'quit':
            exit = True
    
    print("Shutting down client connection.")
    c.close()


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
            if command == 'quit':
                break
            message += " {}".format(command)
        
        commandList = []
        print(message)
        c.send(message.encode())
        time.sleep(1)
    
    print("Shutting down graphics connection.")
    c.close()


if __name__ == "__main__":
    
    #connect to graphics
    print('Waiting for Graphics Server...')
    graphicsSocket = socket.socket()
    port = 12344
    graphicsSocket.bind(('', port))
    graphicsSocket.listen(5)
    g, addrG = graphicsSocket.accept()
    print('Got Graphics connection from', addrG)
    
    #connect to client
    print("Waiting for CLient...")
    clientSocket = socket.socket()
    clientPort = 12345
    clientSocket.bind(('', clientPort))
    clientSocket.listen(5)
    c, addrC = clientSocket.accept()
    print('Got Client connection from', addrC)
    
    t1 = threading.Thread(target=clientConnection, args=(c,))
    t2 = threading.Thread(target=graphicsConnection, args=(g,))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print("Done with both threads.")



