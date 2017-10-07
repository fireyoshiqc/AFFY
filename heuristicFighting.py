from structs import *
from ai import *

def findClosestPlayer(Player, otherPlayers):
    closest = otherPlayers[0]
    closestDistance = playerDistance(Player, otherPlayers[0])
    for other in otherPlayers:
        distance = playerDistance(Player, other)
        if distance < closestDistance:
            closestDistance = distance
            closest = other
    return closest

def evaluateClosestPlayer(Player, otherPlayers):
    closest = findClosestPlayer(Player, otherPlayers)
    capacityRatio = Player.CarriedRessources / Player.CarryingCapacity
    damage = math.floor(3 + closest.AttackPower - 2 * math.pow((Player.Defense), 0,6))
    getOneShot = Player.Health - damage

    #Ignore the player
    if playerDistance(Player, closest) > 5:
        return 0
    #Flee the player
    if capacityRatio > 0.75 or getOneShot:
        return -10000

    #Attack the player
    if(Player.AttackPower)

def playerDistance(Player, PlayerInfo):
    distanceX = math.fabs(Player.Position.X - PlayerInfo.Position.X)
    distanceY = math.fabs(Player.Position.Y - PlayerInfo.Position.Y)

    return distanceX + distanceY