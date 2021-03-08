import socket, threading, queue, utils
from Task import resolve_task, Task, TaskType


class NetworkInterface:
    def __init__(self, robot_id: str):
        self.host, self.port = '127.0.0.1', 12345
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.curr_task: Task = Task(TaskType.NO_TASK, {})
        self.task_queue = queue.Queue()
        
        # Connect to server
        self.socket.connect((self.host, self.port))
        self.socket.send(utils.encode(robot_id))  # send ID to server
        print("Connected successfully!")
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def __del__(self):
        assert (self.task_queue.qsize() == 0)
        self.socket.close()

    def get_current_task(self) -> Task:
        if self.curr_task.task_type == TaskType.NO_TASK:
            self.curr_task = self.__get_next_task()
        return self.curr_task

    def receive_messages(self):
        while True:
            # message received from server
            data = utils.recvall(self.socket)
            self.task_queue.put(resolve_task(data))

    def send_response(self, response: str) -> None:
        self.socket.send(utils.encode(response))
        self.task_queue.task_done()
        self.curr_task = self.__get_next_task()

    def __get_next_task(self) -> Task:
        try:
            return self.task_queue.get(block=False)
        except queue.Empty:
            return Task(TaskType.NO_TASK, {})
