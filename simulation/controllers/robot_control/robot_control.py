from RobotController import RobotController
import socket

import utils


def movearm():
    IKPY_MAX_ITERATIONS = 4
    TIMESTEP = 128

    # Initialize the Webots Supervisor.
    robot_controller = RobotController(timestep=TIMESTEP)

    was_released = False

    x_pos = -.5 # go close to target in increments of .01
    while robot_controller.step(TIMESTEP) != -1:

        is_present = robot_controller.arm.suction_cup.getPresence()
        is_locked = robot_controller.arm.suction_cup.isLocked()


        if is_present and not was_released and not is_locked:
            robot_controller.arm.suction_cup.lock()
        if is_locked:
            robot_controller.arm.park_parcel()
            if robot_controller.arm.is_parked():
                break
        else:
            robot_controller.lift_motor.setPosition(.73)
            x_pos = robot_controller.arm.try_pickup(x_pos)

# This method is from Ryan's (Client's) server.py
def process(data): # takes in request from server and handles the corresponding function.
    # print(data)
    length, robotid, function, params = data.split(":")
    if function == "move":
        from_node , to_node = params.split(";")
        print(f"Robot is moving from node {from_node} to {to_node}.")
        current, desired = params.split(";")
        return utils.encode(f"Moved {robotid} from node {current} to {desired}.")
    elif function == "move_arm":
        print(f"Robotic arm is moving.")
        movearm()
        return utils.encode(f"Arm moved to pick up package.")
    else:
        return utils.encode("Unknown command!")

# This method is from Ryan's (Client's) server.py
def establishConnection():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))

    while True:
        # message sent to server
        # s.send(message.encode('ascii'))

        # message received from server
        print("Waiting to recieve command...")
        data = utils.recvall(s)
        print("msg recieved: " + data)
        response = process(data)
        s.send(response)
    # close the connection
    s.close()
    
establishConnection()