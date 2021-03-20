import asyncio

from server.CentralServer import CentralServer
from server.Robot import Robot, Size
from server.Scheduler import Scheduler
from networking.NetworkInterface import NetworkInterface
from server.Parcel import Parcel
from server.Shelf import Shelf, ShelfInfo
from server.routing.Graph import Graph
from server.sample_db_output import db_output


class Main:
    async def main(self):
        sched = Scheduler(Graph(db_output))
        robot_size = Size(height=.25, length=.75, width=.7)
        sched.add_free_robot(Robot("2", robot_size, 56))
        sched.add_free_robot(Robot("1", robot_size, 27))
        interface = NetworkInterface()
        self.server = CentralServer(sched, interface)
    def getServer(self):
        return self.server

    async def requestParcel(self):
        server = m.getServer()
        my_shelf = Shelf(1, 2, 26)
        shelf_info = ShelfInfo(my_shelf, 1)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        parcel = Parcel(12., Size(.35, .35, .35), 16, shelf_info)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # if cleanup: 'RuntimeError: There is no current event loop..'
            loop = None
        tsk = loop.create_task(server.move_parcel(parcel, None))

m = Main()

    