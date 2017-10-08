import math

class ActionTypes():
    DefaultAction, MoveAction, AttackAction, CollectAction, UpgradeAction, StealAction, PurchaseAction = range(7)


class UpgradeType():
    CarryingCapacity, AttackPower, Defence, MaximumHealth, CollectingSpeed = range(5)


class TileType():
    Tile, Wall, House, Lava, Resource, Shop = range(6)


class TileContent():

       Empty, Wall, House, Lava, Resource, Shop, Player = range(7)


class Point(object):

    # Constructor
    def __init__(self, X=0, Y=0):
        self.X = X
        self.Y = Y

    # Overloaded operators
    def __add__(self, point):
        return Point(self.X + point.X, self.Y + point.Y)

    def __sub__(self, point):
        return Point(self.X - point.X, self.Y - point.Y)

    def __str__(self):
        return "{{{0}, {1}}}".format(self.X, self.Y)

    def __hash__(self):
        return hash((self.X, self.Y))

    def __eq__(self, other):
        return (self.X, self.Y) == (other.X, other.Y)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)

    # Distance between two Points
    def MahanttanDistance(self, p2):
        delta_x = abs(self.X - p2.X)
        delta_y = abs(self.Y - p2.Y)
        return delta_x + delta_y

    def EulerDistance(self, p2):
        delta_x = abs(self.X - p2.X)
        delta_y = abs(self.Y - p2.Y)
        return math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))


class GameInfo(object):

    def __init__(self):
        self.HouseLocation = None
        self.Map  = None
        self.Players = dict()
        self.Shop = list()
        self.Resources = list()
        self.Lava = list()
        self.Wall = list()
        self.Empties = list()

        # nearest
        self.nearestResource = None
        self.nearestPlayer = None

    def addResource(self, point):
        if point not in self.Resources:
            self.Resources.append(point)

    def addShop(self, point):
        if point not in self.Shop:
            self.Shop.append(point)

    def addWall(self, point):
        if point not in self.Wall:
            self.Wall.append(point)

    def clean(self):
        self.Lava = list()
        self.Players = dict()
        self.Empties = list()


    def addLava(self, point):
        self.Lava.append(point)

    def addEmpty(self, point):
        self.Empties.append(point)

    def addPlayer(self, position, playerInfo):
        self.Players[position] = playerInfo

    def findNearestResource(self, position):
        dist = 20
        for point in self.Resources:
            man = point.MahanttanDistance(position)
            if abs(position.X-point.X)<=8 and abs(position.Y-point.Y)<=8 and man<dist:
                dist = man
                self.nearestResource = point
                
        return self.nearestResource

    def findNearestPlayer(self, position):
        for (point, playerInfo) in self.Players:
            man = point.MahanttanDistance(position)
            if abs(position.X-point.X)<=8 and abs(position.Y-point.Y)<=8 and man<dist:
                dist = man
                self.nearestPlayer = (point, playerInfo)
        return self.nearestPlayer


class Tile(object):

    def __init__(self, content=None, x=0, y=0):
        self.Content = content
        self.X = x
        self.Y = y


class Player(object):

    def __init__(self):
        self.Health = 0
        self.MaxHealth = 0
        self.Position = 0
        self.Defense = 0
        self.AttackPower = 0
        self.Score = 0
        self.CarriedRessources = 0
        self.CarryingCapacity = 1000
        self.AttackUpgrades = 0
        self.DefenceUpgrades = 0
        self.CollectingUpgrades = 0
        self.CarryingUpgrades = 0
        self.HealthUpgrades = 0
        self.currentHouseRessources = 0

    def Update(self, health, maxHealth, position, score, defense, attackPower, carriedRessources,
                 carryingCapacity=1000):
        self.Health = health
        self.MaxHealth = maxHealth
        self.Position = position
        self.Defense = defense
        self.AttackPower = attackPower
        self.Score = score
        self.CarriedRessources = carriedRessources
        self.CarryingCapacity = carryingCapacity
    
    def upgrade(self, upgrade):
        if upgrade==UpgradeType.MaximumHealth:
            self.HealthUpgrades += 1
        if upgrade==UpgradeType.AttackPower:
            self.AttackUpgrades += 1
        if upgrade==UpgradeType.Defence:
            self.DefenceUpgrades += 1
        if upgrade==UpgradeType.CollectingSpeed:
            self.CollectingUpgrades += 1
        if upgrade==UpgradeType.CarryingCapacity:
            self.CarryingUpgrades += 1


class PlayerInfo(object):

    def __init__(self, health, maxHealth, position, attackPower, defense, carriedRessources):
        self.Health = health
        self.MaxHealth = maxHealth
        self.Position = position
        self.Defense = defense
        self.AttackPower = attackPower
        self.CarriedRessources = carriedRessources

class ActionContent(object):

    def __init__(self, action_name, content):
        self.ActionName = action_name
        self.Content = str(content)
