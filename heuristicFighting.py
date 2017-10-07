from structs import *
from ai import *
import math

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
    ennemyDamage = math.floor(3 + closest.AttackPower - 2 * math.pow((Player.Defense), 0,6))
    getOneShot = Player.Health - ennemyDamage

    playerDamage = math.floor(3 + Player.AttackPower - 2 * math.pow((closest.Defense), 0,6))
    playerOneShot = closest.Health - playerDamage

    #Ignore the player
    if playerDistance(Player, closest) > 3:
        return 0
    #Flee the player
    if capacityRatio > 0.75 or getOneShot:
        return -10000

    #Attack the player
    if playerOneShot:
        return 1000

def playerDistance(Player, PlayerInfo):
    distanceX = abs(Player.Position.X - PlayerInfo.Position.X)
    distanceY = abs(Player.Position.Y - PlayerInfo.Position.Y)

    return distanceX + distanceY