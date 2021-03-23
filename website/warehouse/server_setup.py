import asyncio

from server.CentralServer import CentralServer
from server.Robot import Robot, Size
from server.Scheduler import Scheduler
from networking.NetworkInterface import NetworkInterface
from server.Parcel import Parcel
from server.Shelf import Shelf, ShelfInfo
from server.routing.Graph import Graph
from server.sample_db_output import db_output


interface = NetworkInterface()
sched = Scheduler(Graph(db_output))
server = CentralServer(sched, interface)
robot_size = Size(height=.25, length=.75, width=.7)
sched.add_free_robot(Robot("2", robot_size, 56))
sched.add_free_robot(Robot("1", robot_size, 27))


def addRobot():
    pass
    #robot_size = Size(height=.25, length=.75, width=.7)
    #sched.add_free_robot(Robot("2", robot_size, 56))
    #sched.add_free_robot(Robot("1", robot_size, 27))


def requestParcel(parcel):
    server.move_parcel(parcel, None)