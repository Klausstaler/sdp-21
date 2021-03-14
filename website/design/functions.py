from .models import package,robot,shelf,hidden_package
from .models import task as tsk
from .models import node as nd
import asyncio
# from warehouse_generator import create_world

def sim_json(json):
    # floor_size = [4,4]
    print('aaaa')

    import sys
    sys.path.insert(0, "../../Warehouse\ Generation/warehouse_generator.py")
    sys.path.insert(0, "../../Warehouse\ Generation/json_parser.py")

    import json_parser as js
    import create_world

    file = open("../../Warehouse\ Generation/json.txt", "w")
    file.write(json)
    file.close()

    shelf_size = [1, 1, 1]
    number_of_racks = 3
    line_distance_from_shelf = 0.2
    # grid_array = [
    #     [2,2,2,5],
    #     [5,5,5,5],
    #     [5,6,6,5],
    #     [6,6,6,6],
    #     ]

    floor_size = js.grid[1]  # gets values from json.txt
    grid_array = js.grid[0]
    print(floor_size)
    print(grid_array)
    create_world("warehouse.wbt", floor_size, shelf_size, number_of_racks, line_distance_from_shelf, grid_array)
    print("World Successfully generated.")
    # pass

def package_request(packs):
    for id in packs:
        pack = packs.get(id)
        print('Parcel:{}'.format(pack.old_id))
        print('Shelf:{}'.format(pack.shelf))
        print('Node:{}'.format(pack.shelf.node))


def get_node_list():
    nodes = []
    for n in nd.objects.all():
        n_of_nodes = 0
        if n.fifth_node:
            n_of_nodes+=1
        if n.fourth_node:
            n_of_nodes+=1
        if n.third_node:
            n_of_nodes+=1
        if n.second_node:
            n_of_nodes+=1
        if n.first_node:
            n_of_nodes+=1
        if n_of_nodes == 5:
            nod = [n.id,n.first_node.id,n.second_node.id,n.third_node.id,n.fourth_node.id,n.fifth_node.id]
        elif n_of_nodes == 4:
            nod = [n.id,n.first_node.id,n.second_node.id,n.third_node.id,n.fourth_node.id]
        elif n_of_nodes == 3:
            nod = [n.id,n.first_node.id,n.second_node.id,n.third_node.id]
        elif n_of_nodes == 2:
            nod = [n.id,n.first_node.id,n.second_node.id]
        elif n_of_nodes == 1:
            nod = [n.id,n.first_node.id]
        nodes.append(nod)
    return nodes

def get_node_dict():
    nodes = {}
    for n in nd.objects.all():
        n_of_nodes = 0
        if n.fifth_node:
            n_of_nodes+=1
        if n.fourth_node:
            n_of_nodes+=1
        if n.third_node:
            n_of_nodes+=1
        if n.second_node:
            n_of_nodes+=1
        if n.first_node:
            n_of_nodes+=1
        if n_of_nodes == 5:
            nod = [n.first_node.id,n.second_node.id,n.third_node.id,n.fourth_node.id,n.fifth_node.id]
        elif n_of_nodes == 4:
            nod = [n.first_node.id,n.second_node.id,n.third_node.id,n.fourth_node.id]
        elif n_of_nodes == 3:
            nod = [n.first_node.id,n.second_node.id,n.third_node.id]
        elif n_of_nodes == 2:
            nod = [n.first_node.id,n.second_node.id]
        elif n_of_nodes == 1:
            nod = [n.first_node.id]
        nodes[n.id] = nod
    return nodes

def get_connected_nodes(id):
    dictionary = get_node_dict()
    return dictionary.get(id)