from collections import namedtuple
from typing import Dict

from server.Robot import Robot
from server.Task import Task, TaskType
import socket
from _thread import start_new_thread
import threading
from server.networking.utils import recvall, encode, decode

print_lock = threading.Lock()

Connection = namedtuple("Connection", ["socket", "address"])


def format_task(robot_id, task: Task) -> str:
    task_type_to_func = {TaskType.MOVE_ARM: "move_arm", TaskType.RAISE_PLATFORM: "raise_platform"}
    res = [robot_id, task_type_to_func[task.task_type]]
    for key, val in task.params.items():
        res.append(val)
    # if no parameters are present, we insert the empty string at the end to present having no params
    if len(task.params) == 0:
        res.append("")
    return ":".join(map(str, res))


# thread function
def send_task(socket: socket.socket, robot_id, task: Task):
    cmd = encode(format_task(robot_id, task))
    # data received from client
    socket.send(cmd)
    response = recvall(socket)
    print_lock.release()
    print(decode(response))


class NetworkInterface:
    """
    Class representing the network interface. Dummy class for now!
    """

    def __init__(self):
        self.central_server = None
        self.port, self.host = 12345, ""
        self.open_connections: Dict[int, Connection] = dict()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind((self.host, self.port))
        print("socket binded to port", self.port)
        self.socket.listen(5)
        print("socket is listening")

    def register_server(self, central_server):
        self.central_server = central_server

    async def send_request(self, robot: Robot, task: Task):
        connection = self.resolve_connection(robot.id)
        print_lock.acquire()
        print('Connected to :', connection.address[0], ':', connection.address[1])
        # start_new_thread(threaded, (connection.socket, robot.id, task)) # let's not thread for now
        send_task(connection.socket, robot.id, task)
        print("Robot", robot.id, "finished task", task.task_type)
        await self.central_server.finished_task(robot)

    def resolve_connection(self, robot_id) -> Connection:
        if robot_id in self.open_connections:
            return self.open_connections[robot_id]
        c, addr = self.socket.accept()  # let's for now hope the next robot connecting is the correct one
        connection = Connection(c, addr)
        self.open_connections[robot_id] = connection
        return connection
