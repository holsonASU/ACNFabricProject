from datetime import datetime as dt
import datetime
import matplotlib.pyplot as plt
import numpy as np
import statistics


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

def getBandwidth(filename):
    
    f = open(filename, 'r')
    
    line = f.readline()
    
    minTime = dt.strptime(line.split('|')[1][:-1], "%Y-%m-%d %H:%M:%S.%f")
    
    bandwidths = list()
    
    count = 0
    
    for line in f:
        
        time = dt.strptime(line.split('|')[1][:-1], "%Y-%m-%d %H:%M:%S.%f")
        
        if time >= (minTime + datetime.timedelta(seconds=1)):
            bandwidths.append(float(count/1000))
            minTime = time
            count = 0
        
        count = count + int(line.split('|')[0])
        
    return bandwidths


experiment = 0

for experiment in range(12):

    clientFileName = 'Outputs/client{}.txt'.format(experiment)
    graphicsFileName = 'Outputs/graphic{}.txt'.format(experiment)  
    
    #print(getAverageRTT(clientFileName))
    
    frameRates = getFrameRate(graphicsFileName)
    bandwidths = getBandwidth(graphicsFileName)
    
    avgRTT = getAverageRTT(clientFileName)
    avgFR = statistics.fmean(frameRates)
    avgBW = statistics.fmean(bandwidths)
    
    output = "{},{},{},{}".format(experiment, avgRTT, avgFR, avgBW)
    print(output)
    
    plt.plot(frameRates)
    plt.xlabel("Time Elapsed (s)")
    plt.ylabel("Frame Rate (frames per second)")
    plt.ylim(0, 150)
    plt.title("Frame Rates for Experiment {}".format(experiment))
    plt.savefig("Outputs/FrameRate{}.png".format(experiment))
    
    plt.clf()
    plt.plot(bandwidths)
    plt.xlabel("Time Elapsed (s)")
    plt.ylabel("Bandwidths (kb)")
    plt.ylim(0, 600)
    plt.title("Bandwidth for Experiment {}".format(experiment))
    plt.savefig("Outputs/Bandwidth{}.png".format(experiment))
    plt.clf()
            
    
