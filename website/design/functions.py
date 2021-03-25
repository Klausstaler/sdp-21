from .models import package,robot,shelf,hidden_package
from .models import task
from .models import node as nd
import sys

sys.path.insert(0, "../Warehouse Generation/")
from server.CentralServer import CentralServer
from server.Robot import Robot, Size
from server.Scheduler import Scheduler
from networking.NetworkInterface import NetworkInterface
from server.Parcel import Parcel
from server.Shelf import Shelf, ShelfInfo
from server.routing.Graph import Graph
from server.sample_db_output import db_output
from warehouse.server_setup import requestParcel,addRobots
import threading
#from warehouse_generator import create_world
import json_parser as js
from warehouse_generator import create_world

def sim_json(json):
    # floor_size = [4,4]

    # sys.path.insert(0, "../Warehouse Generation/json_parser.py")


    print("Sim JSON")

    file = open("../Warehouse Generation/json.txt", "w+")
    file.write(json)
    file.close()


    print(1)

    shelf_size = [1, 1, 1]
    number_of_racks = 3
    line_distance_from_shelf = 0.2
    # grid_array = [
    #     [2,2,2,5],
    #     [5,5,5,5],
    #     [5,6,6,5],
    #     [6,6,6,6],
    #     ]

    floor_size = js.grid()[1]  # gets values from json.txt
    grid_array = js.grid()[0]
    print(floor_size)
    print(grid_array)
    create_world("warehouse.wbt", floor_size, shelf_size, number_of_racks, line_distance_from_shelf, grid_array)
    print("World Successfully generated.")
    # pass

def get_connected_nodes(id):
    dictionary = get_node_dict()
    return dictionary.get(id)

def create_task(r,p,h):
    task.objects.create(robot=r,package=p,holding_package=h)

def package_request(packs):
    testing = False
    if testing:
        addRobots()
        my_shelf = Shelf(1, 2, 26)
        shelf_info = ShelfInfo(my_shelf, 1)
        parcel = Parcel(12., Size(.35, .35, .35), 16, shelf_info)
        # Create parcel instance from the package
        parcel = Parcel(12., Size(.35, .35, .35), 16, shelf_info)
        t = threading.Thread(target=requestParcel, args=(parcel,), daemon=True)
        t.start()
    else:
        addRobots()
        for id in packs:
            pack = packs.get(id)
            #print('Parcel:{}'.format(pack.old_id))
            #print('Shelf:{}'.format(pack.shelf))
            #print('Node:{}'.format(pack.shelf.node))
            #Get the shelf the node is in
            shelf = pack.shelf
            #Create shelf instance
            my_shelf = Shelf(shelf.compartment_size, shelf.number_of_compartments, shelf.node.id)
            #Shelf_info from the shelf
            shelf_info = ShelfInfo(my_shelf, pack.shelf_compartment)
            # Create parcel instance from the package
            parcel = Parcel(pack.weight, Size(.35, .35, .35), shelf.node.id, shelf_info)
            #t = threading.Thread(target=requestParcel, args=(id, parcel,), daemon=True)
            #t.start()
            requestParcel(id,parcel)