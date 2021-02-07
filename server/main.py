import socket
from _thread import *
import threading

print_lock = threading.Lock()

def create_header(zerobits, length): #returns the msg len header of the payload where len = len of msg and zerobits is number of padded zeros at the start
    string = ""
    for i in range(zerobits):
        string += "0"
    string += str(length)
    # print(string)
    return string

def encode(string): # encodes a string in the format msglen:string\n where msglen is len of string
    length = len(string)
    bitlen = len(str(length))
    zerobits = 5 - bitlen
    head = create_header(zerobits,length)
    # print(f"{head}:{str}")
    return f"{head}:{string}\n".encode()

def decode(String): # decodes and returns the string of a recieved msg
    len, msg = String.split(":")
    # print
    return msg

# thread function
def threaded(c): # runs a thread for a single client connection
    while True:
        cmd_str = input("What would you like to do? please format as robotid:function:params\n")
        cmd = encode(cmd_str)
        # print(cmd)
        # data received from client
        c.send(cmd)
        response = recvall(c)
        if not response:
            print('Bye')
            print_lock.release()
            break
        print(decode(response))

    c.close()

def recvall(connection): # handles the reception of packets and decodes the data
    data = b""
    while "\n" not in data.decode():
        data += connection.recv(8)
    # print(data.decode())
    return data.decode()

def Main(): # main func, sets up server, listens for connections and starts a thread for each client connected.
    host = ""

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
