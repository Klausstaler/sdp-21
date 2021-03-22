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
        self.sched = Scheduler(Graph(db_output))
        self.interface = NetworkInterface()
        self.server = CentralServer(self.sched, self.interface)
    def getServer(self):
        return self.server
    def addRobot(self):
        robot_size = Size(height=.25, length=.75, width=.7)
        self.sched.add_free_robot(Robot("2", robot_size, 56))
        self.server = CentralServer(self.sched, self.interface)
    async def requestParcel(self,parcel):
        server = m.getServer()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # if cleanup: 'RuntimeError: There is no current event loop..'
            loop = None
        tsk = loop.create_task(server.move_parcel(parcel, None))

m = Main()

    