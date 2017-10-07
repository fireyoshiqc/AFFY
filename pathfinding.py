import math
from collections import deque
from structs import *

class Node:
    def __init__(self, tile):
        self.tile =tile
        self.parent = None
        self.H = 0
        self.G = 0
    

def enfants(point, grid):
    liens = [grid[d[0]][d[1]] for d in [(point.X-1, point.Y),(point.X,point.Y-1),(point.X,point.Y+1),(point.X+1,point.Y)]]
    return [lien for lien in liens if lien.Content == TileContent.Empty]

def manhattan(point1, point2):
    return abs(point1.X - point2.X) + abs(point1.Y - point2.Y)

def a_star(gamemap, player, target):
    closedset = set()
    openset = set()
    current = gamemap[player.Position.X][player.Position.Y]
    openset.add(current)
    
    while(openset):
        current = min(openset, key=lambda o:o.G + o.H)
        if current == target: #Quand le but est trouvé, on dépile les cases trouvées
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current) #À vérifier
            return path[::-1] #On retourne le résultat renversé
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
                node.H = manhattan(node.tile.Position, target)
                node.parent = current
                openset.add(node)
    return []
