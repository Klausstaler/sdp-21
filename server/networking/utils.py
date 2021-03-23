def create_header(zerobits,
                  length):  # returns the msg len header of the payload where len = len of msg and zerobits is number of padded zeros at the start
    string = ""
    for i in range(zerobits):
        string += "0"
    string += str(length)
    # print(string)
    return string


def encode(string):  # encodes a string in the format msglen:string\n where msglen is len of string
    length = len(string)
    bitlen = len(str(length))
    zerobits = 5 - bitlen
    head = create_header(zerobits, length)
    # print(f"{head}:{str}")
    return f"{head}:{string}\n".encode()


def decode(string: str) -> str:  # decodes and returns the string of a recieved msg
    len, msg = string.split(":")
    # print
    return msg.strip()

def recvall(connection) -> str: # handles the reception of packets and decodes the data
    data = b""
    while "\n" not in data.decode():
        data += connection.recv(8)
    # print(data.decode())
    return data.decode()