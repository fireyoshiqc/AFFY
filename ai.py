from flask import Flask, request
from structs import *
import json
import numpy
import sys
from pathfinding import a_star
from miningCapacity import *
app = Flask(__name__)


gameInfo = GameInfo()
player = Player()

def display_map(gamemap, joueur):
    for row in gamemap:
        srow = ""
        for tile in row:
            if tile.Content == TileContent.Empty:
                srow += "."
            elif tile.Content == TileContent.House:
                srow += "H"
            elif tile.Content == TileContent.Lava:
                srow += "L"
            elif tile.Content == TileContent.Player:
                if Point(tile.X, tile.Y) == player.Position:
                    srow += "I"
                else:
                    srow += "P"
            elif tile.Content == TileContent.Resource:
                srow += "R"
            elif tile.Content == TileContent.Shop:
                srow += "S"
            elif tile.Content == TileContent.Wall:
                srow += "W"
        print srow
    print "Position du joueur:", str(joueur.Position)

def create_action(action_type, target):
    actionContent = ActionContent(action_type, target.__dict__)
    return json.dumps(actionContent.__dict__)

def create_move_action(target):
    return create_action("MoveAction", target)

def create_attack_action(target):
    return create_action("AttackAction", target)

def create_collect_action(target):
    return create_action("CollectAction", target)

def create_steal_action(target):
    return create_action("StealAction", target)

def create_heal_action():
    return create_action("HealAction", "")

def create_purchase_action(item):
    return create_action("PurchaseAction", item)

def create_upgrade_action(upgrade):
    return create_action("UpgradeAction", upgrade)

def check_mining_upgrades():
    currentSpeedUpgrade = player.CollectingUpgrades
    currentCarryingUpgrade = player.CarryingUpgrades
    upgrade = nextUpgrade(10, currentSpeedUpgrade, currentCarryingUpgrade)
    if upgrade is "max":
        return 0
    elif upgrade is "capacity":
        cost = upgradeCost(player.CarryingUpgrades)
    else:
        cost = upgradeCost(player.CollectingUpgrades)
    cash = player.currentHouseRessources
    if(cash >= cost and upgrade is "capacity"):
        player.currentHouseRessources = 0
        return 1
    elif(cash >= cost and upgrade is "speed"):
        player.currentHouseRessources = 0
        return 2
    else:
        return 0

def checkHouse():
    if player.Position == gameInfo.HouseLocation:
        return True
    else:
        return False

def deserialize_map(serialized_map):
    """
    Fonction utilitaire pour comprendre la map
    """
    gameInfo.clean()

    serialized_map = serialized_map[1:]
    rows = serialized_map.split('[')
    column = rows[0].split('{')
    deserialized_map = [[Tile() for x in range(20)] for y in range(20)]
    for i in range(len(rows) - 1):
        column = rows[i + 1].split('{')

        for j in range(len(column) - 1):
            infos = column[j + 1].split(',')
            end_index = infos[2].find('}')
            content = int(infos[0])
            x = int(infos[1])
            y = int(infos[2][:end_index])
            deserialized_map[i][j] = Tile(content, x, y)

            # Add info into gameInfo
            # Get rid off empty resources
            if Point(x, y) in gameInfo.Resources and content != TileContent.Resource:
                gameInfo.Resources.remove(Point(x, y))
            if content == TileContent.Resource:
                gameInfo.addResource(Point(x, y))
            elif content == TileContent.Wall:
                gameInfo.addWall(Point(x, y))
            elif content == TileContent.Lava:
                gameInfo.addLava(Point(x, y))
            elif content == TileContent.Shop:
                gameInfo.addShop(Point(x, y))
            elif content == TileContent.Empty:
                gameInfo.addEmpty(Point(x, y));


    return deserialized_map

def move_to(gamemap, player, target):
    path = a_star(gamemap, player, target)
    if path:
        next_tile = path.pop().tile
        print next_tile.X 
        print next_tile.Y
        return create_move_action(Point(next_tile.X, next_tile.Y))
    else:
        return create_move_action(Point(player.Position.X, player.Position.Y))

def bot():
    """
    Main de votre bot.
    """
    print("Speed: " + str(player.CollectingUpgrades))
    print("Capacity: " + str(player.CarryingUpgrades))
    print("Total cash: " + str(player.currentHouseRessources))

    if checkHouse():
        buyMining = check_mining_upgrades()
        if(buyMining == 1):
            return create_upgrade_action("CarryingCapacity")
        elif(buyMining == 2):
            return create_upgrade_action("CollectingSpeed")

    map_json = request.form["map"]

    # Player info
    encoded_map = map_json.encode()
    map_json = json.loads(encoded_map)
    p = map_json["Player"]
    pos = p["Position"]
    x = pos["X"]
    y = pos["Y"]
    score = p["Score"]
    house = p["HouseLocation"]
    gameInfo.HouseLocation = Point(house["X"], house["Y"])

    player.Update(p["Health"], p["MaxHealth"], Point(x,y),
                    score, int(p["Defence"]), int(p["AttackPower"]),
                    p["CarriedResources"], p["CarryingCapacity"])

    # Map
    serialized_map = map_json["CustomSerializedMap"]
    deserialized_map = deserialize_map(serialized_map)

    # Clear players et lava


    # otherPlayers = []

    # Get info for players
    for player_dict in map_json["OtherPlayers"]:
        for player_name in player_dict.keys():
            player_info = player_dict[player_name]
            if player_info == 'notAPlayer': continue
            p_pos = player_info["Position"]
            gameInfo.addPlayer(Point(p_pos["X"], p_pos["Y"]), PlayerInfo(player_info["Health"], player_info["MaxHealth"],
                                                                         Point(p_pos["X"], p_pos["Y"]), player_info["AttackPower"],
                                                                         player_info["Defence"], player_info["Resources"]))
            # player_info = PlayerInfo(player_info["Health"],
            #                          player_info["MaxHealth"],
            #                          Point(p_pos["X"], p_pos["Y"]))

            # otherPlayers.append({player_name: player_info })

    display_map(deserialized_map, player)
    # return move_to(deserialized_map, player, Point(30,30))
    return decideMove(deserialized_map)

def findEmptySpot(x,y):
    dist = 20
    ret = None
    for i in range(x-1, x+1):
        for j in range(y-1, y+1):
            point = Point(i,j)
            man = point.MahanttanDistance(player.Position)
            if (point in gameInfo.Empties and man < dist):
                dist = man
                ret = point
    return ret

def decideMove(deserialized_map):
    gameInfo.findNearestResource(player.Position)
    if gameInfo.nearestResource is None:
        return move_to(deserialized_map, player, Point(player.Position.X, player.Position.Y - 1))
        
    else:
        if player.CarriedRessources < player.CarryingCapacity:
            x = gameInfo.nearestResource.X
            y = gameInfo.nearestResource.Y
            distNearestResource = player.Position.MahanttanDistance(gameInfo.nearestResource)
            print("Nearest resource: (", gameInfo.nearestResource.X, gameInfo.nearestResource.Y, ")", distNearestResource)
            if (distNearestResource == 1):
                print "MINING"
                print str(player.CarriedRessources)
                player.currentHouseRessources += 100*returnSpeed(player.CollectingUpgrades)
                return create_collect_action(gameInfo.nearestResource)
            elif (distNearestResource > 1):
                empty_spot = findEmptySpot(x,y)
                if empty_spot:
                    return move_to(deserialized_map, player, findEmptySpot(x,y))
                else:
                    return move_to(deserialized_map, player, gameInfo.HouseLocation)
        else:
            return move_to(deserialized_map, player, gameInfo.HouseLocation)



@app.route("/", methods=["POST"])
def reponse():
    """
    Point d'entree appelle par le GameServer
    """
    return bot()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


