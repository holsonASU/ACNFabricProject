from datetime import datetime as dt
import datetime
import matplotlib.pyplot as plt
import numpy as np


def getClientTimes(file):
    
    clientFile = open(file, 'r')
    clientSent = dict()
    clientReceived = dict()
    
    for line in clientFile:
        
        l = line.split("@")
        
        if l[0] == "s":
            #sent
            d = l[1].split("|")
            clientSent[d[0]] = d[1][:-1]
            
        else:
            #received
            d = l[1].split("|")
            for x in d[0].split(","):
                if x is not "":
                    clientReceived[x] = d[1][:-1]
                
    clientFile.close()
    return clientSent, clientReceived



def getAverageRTT(filename):
    
    clientSent, clientReceived = getClientTimes(filename)
    
    RTTList = list()
    
    for k,v in clientSent.items():
        
        if k in clientReceived:
            duration = dt.strptime(clientReceived.get(k), "%Y-%m-%d %H:%M:%S.%f") - dt.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
            RTTList.append(duration)
    
    total = 0
    for r in RTTList:
        total = total + r.microseconds
    
    return (total/1000)/len(RTTList)

def getFrameRate(filename):
    
    f = open(filename, 'r')
    
    line = f.readline()
    
    minTime = dt.strptime(line.split('|')[1][:-1], "%Y-%m-%d %H:%M:%S.%f")
    
    frameRates = list()
    
    count = 0
    for line in f:
        
        time = dt.strptime(line.split('|')[1][:-1], "%Y-%m-%d %H:%M:%S.%f")
        
        if time >= (minTime + datetime.timedelta(seconds=1)):
            frameRates.append(count)
            minTime = time
            count = 0
        
        count = count + 1
        
    return frameRates


clientFileName = 'Outputs/client{}.txt'.format(0)
graphicsFileName = 'Outputs/graphic{}.txt'.format(0)  

print(getAverageRTT(clientFileName))

frameRates = getFrameRate(graphicsFileName)

plt.plot(frameRates)
plt.xlabel("Time Elapsed (s)")
plt.ylabel("Frame Rate (frames per second)")
plt.ylim(0, 150)
            
    
