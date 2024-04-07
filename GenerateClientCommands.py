import random

fileName = "clientCommands2.txt"

f = open(fileName, "w")

totalTime = 0

while totalTime <= 60:
    
    line = ""
    for x in range(14):
        y = random.random()
        if y < .5:
            line = line + "True,"
        else:
            line = line + "False,"
    
    for x in range(6):
        y = random.triangular(-1, 1)
        line = line + str(y) +','
    
    waitTime = random.triangular(0, 1)
    totalTime = totalTime + waitTime
    line = line + "|" + str(waitTime) + '\n'
    f.write(line)
    
f.write("quit|0")
f.close()
    
    
    
    
