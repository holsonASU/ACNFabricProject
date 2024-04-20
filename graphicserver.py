import socket
import sys
import random
import time
#import cv2
import datetime

def logCommandReceived(indices):
    if len(indices) > 0:
        f = open("graphicsCommandLog.txt", 'a')
        line = indices + '|' + str(datetime.datetime.now()) + '\n'
        f.write(line)
        f.close()
        
def loadImage(file):
    #cap = cv2.imread(file)
    f = open(file, 'rb')
    img = f.read()
    f.close()
    return img

logicIP = 'localhost'
videoFile = 'Videos/1080.png'

if len(sys.argv) > 1:
    logicIP = sys.argv[1]
    videoFile = sys.argv[2]

#open video
#image = loadImage(videoFile)

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
    try:
        message = str(logicSocket.recv(1024).decode())
        
        indices = message.split('@')[0]
        logCommandReceived(indices)
        
        print(indices + '|' + str(datetime.datetime.now()))
        
        if "quit" in message.lower():
            c.send("quit".encode())
            print("Quit has been received.")
            break
        
        #render scene
        #print('sleeping')
        
        renderTime = random.gauss(8.33, 0.32) / 1000
        time.sleep(renderTime)
        #print('out of sleep')
        c.send(indices.encode())
        #print('sent index')
        #c.send(image.tobytes())
        #print('sent frame')
        #c.send('!'.encode())
    except:
        done = True

logicSocket.close()
s.close()
print("Graphics Exited Gracefully.")