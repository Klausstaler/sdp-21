import threading

from server.CentralServer import CentralServer
from server.Robot import Robot, Size
from server.Scheduler import Scheduler
from networking.NetworkInterface import NetworkInterface
from server.Parcel import Parcel
from server.Shelf import Shelf, ShelfInfo
from server.routing.Graph import Graph
from server.sample_db_output import db_output


def main():
    sched = Scheduler(Graph(db_output))
    my_shelf = Shelf(1, 2, 26)
    shelf_info = ShelfInfo(my_shelf, 1)
    parcel = Parcel(12., Size(.35, .35, .35), 16, shelf_info)
    robot_size = Size(height=.25, length=.75, width=.7)
    sched.add_free_robot(Robot("2", robot_size, 56))
    sched.add_free_robot(Robot("1", robot_size, 27))
    interface = NetworkInterface()
    server = CentralServer(sched, interface)
    task1 = threading.Thread(target=server.move_parcel, args=(parcel, None), daemon=True)
    my_shelf = Shelf(1, 2, 38)
    shelf_info = ShelfInfo(my_shelf, 1)
    parcel = Parcel(12., Size(.35, .35, .35), 38, shelf_info)
    task2 = threading.Thread(target=server.move_parcel, args=(parcel, None), daemon=True)
    task1.start()
    task2.start()
    task1.join()
    task2.join()


if __name__ == "__main__":
    main()
