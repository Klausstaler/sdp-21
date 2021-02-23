import socket, threading, queue, utils
from Task import resolve_task

class NetworkInterface:
    def __init__(self):
        self.host, self.port = '127.0.0.1', 12345
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server
        self.socket.connect((self.host, self.port))
        print("Connected successfully!")
        self.task_queue = queue.Queue()
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def __del__(self):
        assert(self.task_queue.qsize() == 0)
        self.socket.close()

    def receive_messages(self):
        while True:
            # message received from server
            print("Waiting to receive command...")
            data = utils.recvall(self.socket)
            print("msg received: " + data)
            self.task_queue.put(resolve_task(data))

    def send_response(self, response: str) -> None:
        self.socket.send(utils.encode(response))