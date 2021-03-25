import json

# usage: paste json output from web interface into json.txt and load this module and reference the grid variable
# to return the respective matrix/dimensions for webots file generation.


class Node:
    def __init__(self, id, type, neighbours, coords): # Class to store information on a node
        self.id = id
        self.type = type
        self.neighbours = neighbours
        self.coords = coords

        self.up = -1
        self.right = -1
        self.down = -1
        self.left = -1

        self.set_neighbours()
        self.junction_type = self.get_junction_number()


    def get_junction_number(self): # gets the respective value for the node texture depending on its connection and type
        # print(self.type)
        if self.type == "shelf":
            if self.up != -1:
                return 0
            elif self.down != -1:
                return 2
            elif self.left != -1:
                return 3
            elif self.right != -1:
                return 1

        # elif self.type == "Robot": # needs updated
        #     return 15

        elif self.type == "rfid":

            if (self.up != -1 and self.right == -1 and self.down != -1 and self.left == -1) or (self.right == -1 and self.left == -1 and (self.up != -1 or self.down != -1)): # vertical
                return 5
            if (self.up == -1 and self.right != -1 and self.down == -1 and self.left != -1) or (self.up == -1 and self.down == -1 and (self.right != -1 or self.left != -1)): # horizontal
                return 4
            if self.up != -1 and self.right != -1 and self.down != -1 and self.left != -1: # 4-Way connection
                return 6
            if self.up != -1 and self.right != -1 and self.down == -1 and self.left == -1: # junction: NE
                return 13
            if self.up != -1 and self.right != -1 and self.down == -1 and self.left != -1: # NEW
                return 10
            if self.up != -1 and self.right == -1 and self.down == -1 and self.left != -1: # NW
                return 14
            if self.up == -1 and self.right == -1 and self.down != -1 and self.left != -1: # SW
                return 11
            if self.up == -1 and self.right != -1 and self.down != -1 and self.left == -1: # SE
                return 12
            if self.up != -1 and self.right == -1 and self.down != -1 and self.left != -1: # NSW
                return 7
            if self.up == -1 and self.right != -1 and self.down != -1 and self.left != -1: # ESW
                return 9
            if self.up != -1 and self.right != -1 and self.down != -1 and self.left == -1: # NSE
                return 8



    def set_neighbour(self, direction, present): # assigns a direction to a neighbouring node.
            if direction == "up":
                if present != -1:
                    self.up = self.neighbours["up"]
                else:
                    self.up = -1
            elif direction == "down":
                if present != -1:
                    self.down = self.neighbours["down"]
                else:
                    self.down = -1
            elif direction == "left":
                if present != -1:
                    self.left = self.neighbours["left"]
                else:
                    self.left = -1
            elif direction == "right":
                if present != -1:
                    self.right = self.neighbours["right"]
                else:
                    self.right = -1

    def set_neighbours(self):  # assigns a direction to all neighbouring node if they exist.
        for i in ["up", "down", "left", "right"]:
            if i in self.neighbours.keys():
                self.set_neighbour(i, 1)
            else:
                self.set_neighbour(i, -1)

class Payload(object): # takes a raw json string and parses it into a list of nodes and dimensions
    def __init__(self, string):
        self.str = string
        self.__dict__ = json.loads(string)
        self.nodes = self.get_nodes()
        self.dimensions = self.__dict__["dimensions"]
    def get_nodes(self):
        nodes = []
        for i in self.__dict__["nodes"].keys():
            # print("ID: " + i )
            id = i
            type = self.__dict__["nodes"][i]["type"]
            coords = self.__dict__["nodes"][i]["coords"]
            neighbours = self.__dict__["nodes"][i]["neighbours"]
            nodes.append(Node(i,type,neighbours, coords))
        return nodes

def get_coords(id, nodes): # returns a nodes coords given its id
    # print(id)
    for i in nodes:
        if i.id == str(id):
            return i.coords
    return [0,0]

# def get_id(id, coords): # returns a nodes coords given its id
#     # print(id)
#     for i in:
#         if i.id == str(id):
#             return i.coords
#     return [0,0]

def get_grid(dimensions, nodes): # creates a grid representation of a graph for texture/map generation.
    import numpy as np
    height = dimensions[0]
    width = dimensions[1]
    grid_line = -np.ones([width,height])
    grid_ids = -np.ones([width,height])

    # print(nodes)
    for node in nodes:
        # print(node.junction_type)
        coords = node.coords
        type = node.junction_type
        grid_line[coords[1]][coords[0]] = type
        grid_ids[coords[1]][coords[0]] = node.id


        for neighbour in node.neighbours.keys():
            nodex, nodey = node.coords
            neighbourx, neighboury = get_coords(node.neighbours[neighbour][0], nodes)

            if nodex == neighbourx:
                for i in range (nodey + 1, neighboury):
                    grid_line[i][nodex] = 5
                pass
            elif nodey == neighboury:
                for i in range(nodex + 1, neighbourx):
                    grid_line[nodey][i] = 4
                pass
    # print(grid_ids)
    return grid_line, [width, height], grid_ids

def grid():
    with open("../Warehouse Generation/json.txt", "r") as f:
        string = f.read()
        # print(string)
        p = Payload(string)
    return get_grid(p.dimensions, p.nodes)
