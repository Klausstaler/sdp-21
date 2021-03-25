from server.CentralServer import CentralServer
from server.Robot import Robot, Size
from server.Scheduler import Scheduler
from networking.NetworkInterface import NetworkInterface
from server.Parcel import Parcel
from server.Shelf import Shelf, ShelfInfo
from server.routing.Graph import Graph
from server.routing.containers import Connection, Direction

from design.models import package,robot,shelf,hidden_package
from design.models import task
from design.models import node as nd

import time

def getDirection(dir):
    if dir == 'from':
        direction = Direction.INCOMING
    elif dir == 'to':
        direction = Direction.OUTGOING
    elif dir == 'bi':
        direction = Direction.BIDIRECTIONAL
    return direction
def get_node_dict():
    nodes = {}
    for n in nd.objects.all():
        data = []
        if n.right_node:
            direction = getDirection(n.right_node_direction)
            data.append(Connection(n.right_node.id,n.right_node_distance,n.right_node_priority,direction))
        else:
            data.append(None)
        if n.down_node:
            direction = getDirection(n.down_node_direction)
            data.append(Connection(n.down_node.id,n.down_node_distance,n.down_node_priority,direction))
        else:
            data.append(None)
        if n.left_node:
            direction = getDirection(n.left_node_direction)
            data.append(Connection(n.left_node.id,n.left_node_distance,n.left_node_priority,direction))
        else:
            data.append(None)
        if n.up_node:
            direction = getDirection(n.up_node_direction)
            data.append(Connection(n.up_node.id,n.up_node_distance,n.up_node_priority,direction))
        else:
            data.append(None)
        nodes[n.id] = data
    return nodes

ros = robot.objects.all()
for r in ros:
    r.delete()

interface = NetworkInterface()
sched = Scheduler(Graph(get_node_dict()))
server = CentralServer(sched, interface)
#robot_size = Size(height=.25, length=.75, width=.7)
#sched.add_free_robot(Robot("2", robot_size, 56))
#sched.add_free_robot(Robot("1", robot_size, 27))

def addRobots():
    while True:
        robots = robot.objects.all()
        added_robots = False
        for r in robots:
            if not r.status:
                robot_size = Size(height=r.height, length=r.length, width=r.width)
                sched.add_free_robot(Robot(r.name, robot_size, r.node_id))
                added_robots = True
        if added_robots:
            break
        else:
            print('No free robots can be found.\nWaiting for a robot to become free...')
            time.sleep(2)

def requestParcel(id, parcel):
    server.move_parcel(id, parcel, None)