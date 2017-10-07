import math
from collections import deque
from structs import *
import time

class Node:
    def __init__(self, tile, relX, relY):
        self.tile = tile
        self.parent = None
        self.relX = relX
        self.relY = relY
        self.H = 0
        self.G = 0
    

def enfants(current, grid):
    liens = [grid[d[0]][d[1]] for d in [(current.relX-1, current.relY),(current.relX,current.relY-1),(current.relX,current.relY+1),(current.relX+1,current.relY)]]
    return [Node(lien, current.relX+lien.X-current.tile.X, current.relY+lien.Y-current.tile.Y) for lien in liens if lien.Content == TileContent.Empty]

def manhattan(point1, point2):
    return abs(point1.X - point2.X) + abs(point1.Y - point2.Y)

def a_star(gamemap, player, target):
    coin_map = gamemap[0][0]
    target_rel = Point(0,0)
    

    coords_rel = player.Position.__sub__(coin_map)
    current = Node(gamemap[coords_rel.X][coords_rel.Y], coords_rel.X, coords_rel.Y)
    closedset = set()
    openset = set()
    #current = gamemap[player.Position.X][player.Position.Y]
    openset.add(current)
    
    while(openset):
        current = min(openset, key=lambda o:o.G + o.H)
        if current.tile.X == target.X and current.tile.Y == target.Y: #Quand le but est trouve, on depile les cases trouvees
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            #path.append(current) #A verifier
            return path#[::-1] #On retourne le resultat renverse
        openset.remove(current)
        closedset.add(current)
        for node in enfants(current, gamemap):
            if node in closedset:
                continue
            if node in openset:
                if node.G > current.G + 1:
                    node.G = current.G + 1
                    node.parent = current
            else:
                node.G = current.G + 1
                node.H = manhattan(node.tile, target)
                node.parent = current
                openset.add(node)
    return []
