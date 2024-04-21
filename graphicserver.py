import socket
import sys
import random
import time
import cv2
import datetime
from mlsocket import MLSocket

def logCommandReceived(indices):
    if len(indices) > 0:
        f = open("graphicsCommandLog.txt", 'a')
        line = indices + '|' + str(datetime.datetime.now()) + '\n'
        f.write(line)
        f.close()
        
def loadImage(file):
    #cap = cv2.imread(file)
    cap = open(file, 'rb')
    return cap

logicIP = 'localhost'
videoFile = 'Videos/1080.png'
gpuTimeMean = 8.33
gpuTimeStd = 0.32

if len(sys.argv) > 1:
    logicIP = sys.argv[1]
    videoFile = sys.argv[2]
    gpuTimeMean = float(sys.argv[3])
    gpuTimeStd = float(sys.argv[4])

#open video
image = loadImage(videoFile)

imageSize = sys.getsizeof(image)

#connect to logic node
logicSocket = socket.socket()
logicPort = 12344
logicSocket.connect((logicIP, logicPort))
print("Graphics connected to Logic.")

#listen for client node
s = MLSocket()
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
        
        print(str(imageSize) + '|' + str(datetime.datetime.now()))
        
        if "quit" in message.lower():
            c.send("quit".encode())
            print("Quit has been received.")
            break
        
        #render scene
        #print('sleeping')
        
        renderTime = random.gauss(gpuTimeMean, gpuTimeStd) / 1000
        time.sleep(renderTime)
        #print('out of sleep')
        c.send(indices.encode())
        c.send(image)
        #print('sent index')
        #c.send(image.tobytes())
        #print('sent frame')
        #c.send('!'.encode())
    except:
        done = True

logicSocket.close()
s.close()
print("Graphics Exited Gracefully.")