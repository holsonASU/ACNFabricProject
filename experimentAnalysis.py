from datetime import datetime


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



def getAverageRTT(experiment):
    
    clientFileName = 'logs/clientLog{}.txt'.format(experiment)
    
    clientSent, clientReceived = getClientTimes(clientFileName)
    
    RTTList = list()
    
    for k,v in clientSent.items():
        
        if k in clientReceived:
            duration = datetime.strptime(clientReceived.get(k), "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
            RTTList.append(duration)
    
    total = 0
    for r in RTTList:
        total = total + r.microseconds
    
    return (total/1000)/len(RTTList)
    

print(getAverageRTT(0))
            
    
