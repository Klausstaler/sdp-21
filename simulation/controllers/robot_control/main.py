# Import socket module
import socket

# DAVE - I've moved this to Fredrik's robot_arm.py
#
# def process(data): # takes in request from server and handles the corresponding function.
#     # print(data)
#     length, robotid, function, params = data.split(":")
#     if function == "move":
#         from_node , to_node = params.split(";")
#         print(f"Robot is moving from node {from_node} to {to_node}.")
#         current, desired = params.split(";")
#         return encode(f"Moved {robotid} from node {current} to {desired}.")
#     if function == "move-arm":
#         print(f"Robotic arm is moving.")
#         #robot_arm.move-arm()
#         return encode(f"Arm moved to pick up package.")

# DAVE - I've moved this to Fredrik's robot_arm.py under method establishConnection()
#
# def Main(): # connects to the central server and listens for commands
#     # local host IP '127.0.0.1'
#     host = '127.0.0.1'

#     # Define the port on which you want to connect
#     port = 12345

#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     # connect to server on local computer
#     s.connect((host, port))

#     while True:
#         # message sent to server
#         # s.send(message.encode('ascii'))

#         # messaga received from server
#         print("Waiting to recieve command...")
#         data = recvall(s)
#         print("msg recieved: " + data)
#         response = process(data)
#         s.send(response)
#         # ask the client whether he wants to continue
#         # ans = input('\nDo you want to continue(y/n) :')
#         # if ans == 'y':
#         #     continue
#         # else:
#         #     break
#     # close the connection
#     s.close()


def displayOptions(): # Ignore
    print(f"1. Display_Functions\n2. Enter Function")
    answer = input()
    if answer == str(1):
        file = open("functions.txt", "r")
        line = file.readline()
        print(line)
        while line != "\n":
            print(line)
            line = file.readline()

if __name__ == '__main__':
    Main()
    # displayOptions()