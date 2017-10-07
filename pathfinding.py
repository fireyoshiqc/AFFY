import math
from collections import deque
from structs import *

class Node:
    def __init__(self, tile, X, Y):
        self.tile = tile
        self.parent = None
        self.X = 0
        self.Y = 0
        self.H = 0
        self.G = 0
    

def enfants(coords_rel, point, grid):
    liens = [grid[d[0]][d[1]] for d in [(coords_rel.X-1, coords_rel.Y),(coords_rel.X,coords_rel.Y-1),(coords_rel.X,coords_rel.Y+1),(coords_rel.X+1,coords_rel.Y)]]
    return [Node(lien, coords_rel.X+lien.X-point.X, coords_rel.Y+lien.Y-point.Y) for lien in liens if lien.Content == TileContent.Empty]

def manhattan(point1, point2):
    return abs(point1.X - point2.X) + abs(point1.Y - point2.Y)

def a_star(gamemap, player, target):
    coin_map = gamemap[0][0]
    coords_rel = player.Position.__sub__(coin_map)
    current = Node(gamemap[coords_rel.X][coords_rel.Y], coords_rel.X, coords_rel.Y)
    closedset = set()
    openset = set()
    #current = gamemap[player.Position.X][player.Position.Y]
    openset.add(current)
    
    while(openset):
        current = min(openset, key=lambda o:o.G + o.H)
        print str(openset)
        print str(closedset)
        if current == target: #Quand le but est trouve, on depile les cases trouvees
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current) #A verifier
            return path#[::-1] #On retourne le resultat renverse
        openset.remove(current)
        closedset.add(current)
        for node in enfants(coords_rel, current.tile, gamemap):
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
