from flask import Flask, request
from structs import *
import json
import numpy
import sys

app = Flask(__name__)

gameInfo = GameInfo()

def display_map(gamemap):
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
                srow += "P"
            elif tile.Content == TileContent.Resource:
                srow += "R"
            elif tile.Content == TileContent.Shop:
                srow += "S"
            elif tile.Content == TileContent.Wall:
                srow += "W"
        print srow

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


def deserialize_map(serialized_map):
    """
    Fonction utilitaire pour comprendre la map
    """
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


    return deserialized_map

def bot():
    """
    Main de votre bot.
    """
    map_json = request.form["map"]

    # Player info

    encoded_map = map_json.encode()
    map_json = json.loads(encoded_map)
    p = map_json["Player"]
    pos = p["Position"]
    x = pos["X"]
    y = pos["Y"]
    house = p["HouseLocation"]
    player = Player(p["Health"], p["MaxHealth"], Point(x,y),
                    Point(house["X"], house["Y"]), 0,
                    p["CarriedResources"], p["CarryingCapacity"])

    # Map
    serialized_map = map_json["CustomSerializedMap"]
    deserialized_map = deserialize_map(serialized_map)

    # otherPlayers = []

    for player_dict in map_json["OtherPlayers"]:
        for player_name in player_dict.keys():
            player_info = player_dict[player_name]
            if player_info == 'notAPlayer': continue
            p_pos = player_info["Position"]
            gameInfo.addPlayer(p_pos, float(player_info["Health"])/float(player_info["MaxHealth"]))
            # player_info = PlayerInfo(player_info["Health"],
            #                          player_info["MaxHealth"],
            #                          Point(p_pos["X"], p_pos["Y"]))

            # otherPlayers.append({player_name: player_info })

    # return decision
    display_map(deserialized_map)
    return create_move_action(player.Position.__add__(Point(1,0)))

@app.route("/", methods=["POST"])
def reponse():
    """
    Point d'entree appelle par le GameServer
    """
    return bot()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

