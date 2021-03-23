import socket, threading
import time
from typing import Dict, NamedTuple, Tuple

from networking.utils import encode, decode, recvall
from server.Robot import Robot, Size
from server.Task import Task

from design.models import robot as rbt
from design.models import node

from random import randint

class Connection(NamedTuple):
    socket: socket.socket
    address: Tuple[str, int]


def format_task(robot_id, task: Task) -> str:
    res = [robot_id, task.task_type.value]
    for key, val in task.params.items():
        res.append(",".join(map(str, [key, val])))
    # if no parameters are present, we insert the empty string at the end to present having no params
    if len(task.params) == 0:
        res.append("")
    return ":".join(map(str, res))


# thread function
def send_task(sock: socket.socket, robot_id, task: Task):
    cmd = encode(format_task(robot_id, task))
    # data received from client
    sock.send(cmd)
    response = recvall(sock)
    print(decode(response))


class NetworkInterface:
    """
    Class representing the network interface. Dummy class for now!
    """

    def __init__(self):
        self.port, self.host = 2000, "127.0.0.1"
        self.open_connections: Dict[str, Connection] = dict()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("BINDING SOCKET")
        self.socket.bind((self.host, self.port))
        print("socket binded to port", self.port)
        self.socket.listen(5)
        print("socket is listening")
        threading.Thread(target=self.receive_new_connections, daemon=True).start()

    def __del__(self):
        for k, connection in self.open_connections.items():
            connection.socket.close()
        self.socket.close()

    def receive_new_connections(self):
        while True:
            sock, addr = self.socket.accept()
            connection = Connection(sock, addr)
            robot_id, node_id = decode(recvall(sock)).split(";")
            node_id = int(node_id)
            height = .25; length = .75; width = .7
            size = Size(height=height, length=length, width=width)
            #Add robot to db
            rbt.objects.create(name=str(robot_id),node_id=node.objects.get(pk=node_id),height=height, length=length, width=width)
            #rbt.objects.create(name=str(robot_id),node_id=node.objects.all()[0],height=height, length=length, width=width)
            print(robot_id, node_id, size)
            self.open_connections[robot_id] = connection
            print('Connected to :', connection.address[0], ':', connection.address[1])
            print(f"Robot ID {robot_id}")

    def send_request(self, robot: Robot, task: Task):
        connection = self.resolve_connection(robot.id)
        send_task(connection.socket, robot.id, task)
        #print("Robot", robot.id, "finished task", task.task_type)

    def resolve_connection(self, robot_id) -> Connection:
        if robot_id in self.open_connections:
            return self.open_connections[robot_id]
        else:
            time.sleep(2)
            print(f"No connection with ID {robot_id} found! Sleeping 2 secs..")
            return self.resolve_connection(robot_id)
