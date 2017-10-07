import math

class ActionTypes():
    DefaultAction, MoveAction, AttackAction, CollectAction, UpgradeAction, StealAction, PurchaseAction = range(7)


class UpgradeType():
    CarryingCapacity, AttackPower, Defence, MaximumHealth, CollectingSpeed = range(5)


class TileType():
    Tile, Wall, House, Lava, Resource, Shop = range(6)


class TileContent():
    Empty, Resource, House, Player, Wall, Lava, Shop = range(7)


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

    def clearLava(self):
        self.Lava = list()

    def clearPlayers(self):
        self.Players = dict()

    def addLava(self, point):
        self.Lava.append(point)

    def addPlayer(self, position, healthRatio):
        self.Players[position] = healthRatio

    def nearestResource(self, position):
        dist = 40
        for point in self.Resources:
            if position.MahanttanDistance(point) < dist:
                self.nearestResource = point
        return self.nearestResource

    def nearestPlayer(self, position):
        dist = 40
        for (point, healthRatio) in self.Players:
            if position.MahanttanDistance(point) < dist:
                self.nearestPlayer = (point, healthRatio)

        return self.nearestPlayer


class Tile(object):

    def __init__(self, content=None, x=0, y=0):
        self.Content = content
        self.X = x
        self.Y = y


class Player(object):

    def __init__(self, health, maxHealth, position, houseLocation, score, defense, attackPower, carriedRessources,
                 carryingCapacity=1000):
        self.Health = health
        self.MaxHealth = maxHealth
        self.Position = position
        self.Defense = defense
        self.AttackPower = attackPower
        self.HouseLocation = houseLocation
        self.Score = score
        self.CarriedRessources = carriedRessources
        self.CarryingCapacity = carryingCapacity


class PlayerInfo(object):

    def __init__(self, health, maxHealth, position):
        self.Health = health
        self.MaxHealth = maxHealth
        self.Position = position

class ActionContent(object):

    def __init__(self, action_name, content):
        self.ActionName = action_name
        self.Content = str(content)
