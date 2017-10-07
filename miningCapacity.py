def calculateRatio(distance, speedLevel, capacityLevel):
    moves = distance*2 + returnCapacity(capacityLevel)/(returnSpeed(speedLevel)*100)
    ressources = returnCapacity(capacityLevel)
    return ressources/moves

def returnCapacity(level):
    if level == 0:
        return 1000
    elif level == 1:
        return 1500
    elif level == 2:
        return 2500
    elif level == 3:
        return 5000
    elif level == 4:
        return 10000
    else:
        return 25000

def returnSpeed(level):
    if level == 0:
        return 1
    elif level == 1:
        return 1.25
    elif level == 2:
        return 1.5
    elif level == 3:
        return 2.0
    elif level == 4:
        return 2.5
    else:
        return 3.5

def upgradeCost(level):
    nextLevel = level + 1
    if nextLevel == 1:
        return 15000
    elif nextLevel == 2:
        return 50000
    elif nextLevel == 3:
        return 100000
    elif nextLevel == 4:
        return 250000
    else:
        return 500000


def nextUpgrade(distance, currentSpeedLevel, currentCapacityLevel):
    if(currentSpeedLevel == 5 and currentCapacityLevel < 5):
        return'capacity'
    if (currentCapacityLevel == 5 and currentSpeedLevel < 5):
        return 'speed'
    if(currentCapacityLevel == 5 and currentSpeedLevel == 5 ):
        return 'max'


    ratioSpeed = calculateRatio(distance, currentSpeedLevel+1, currentCapacityLevel)
    ratioCapacity = calculateRatio(distance, currentSpeedLevel, currentCapacityLevel+1)

    speedCost = upgradeCost(currentSpeedLevel+1) / ratioSpeed
    capacityCost = upgradeCost(currentCapacityLevel+1) / ratioCapacity

    if speedCost < capacityCost:
        return "speed"
    else:
        return "capacity"


def test():
    Speed = 0
    Cap = 0
    while (Speed < 6 or Cap < 6):
        next = nextUpgrade(10, Speed, Cap)
        print(next)
        if(next == "speed"):
            Speed += 1
        if (next == "capacity"):
            Cap += 1
        if (next == 'max'):
            break;
test()


            #for i in range(10, 20, 5):
#    for j in range(6):
#        for k in range(6):
#            print("Distance: " + str(i) + " Speed Level: " + str(j) + " CapacityLevel: " + str(k) + " Ressources/Moves Ratio: " + str(calculateRatio(i,j,k)) + " Next Upgrade: " + str())