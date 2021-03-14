from .models import package,robot,shelf,hidden_package
from .models import task
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

def get_node_dict():
    nodes = {}
    for n in nd.objects.all():
        data = {}
        if n.right_node:
            data['right'] = [n.right_node.id,n.right_node_distance,n.right_node_direction,n.right_node_priority]
        if n.left_node:
            data['left'] = [n.left_node.id,n.left_node_distance,n.left_node_direction,n.left_node_priority]
        if n.down_node:
            data['down'] = [n.down_node.id,n.down_node_distance,n.down_node_direction,n.down_node_priority]
        if n.up_node:
            data['up'] = [n.up_node.id,n.up_node_distance,n.up_node_direction,n.up_node_priority]
        nodes[n.id] = data
        print(nodes)
    return nodes

def get_connected_nodes(id):
    dictionary = get_node_dict()
    return dictionary.get(id)

def create_task(r,p,h):
    task.objects.create(robot=r,package=p,holding_package=h)


def package_request(packs):
    for id in packs:
        pack = packs.get(id)
        print('Parcel:{}'.format(pack.old_id))
        print('Shelf:{}'.format(pack.shelf))
        print('Node:{}'.format(pack.shelf.node))
        get_node_dict()
        rob = robot.objects.all()[0]
        create_task(rob,pack,False)