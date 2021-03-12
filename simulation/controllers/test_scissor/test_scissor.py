"""level1 controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from math import asin, sqrt, pi

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())


def movePlatform(H,L,n):
    motors = [robot.getDevice(f"motor {i+1} {j}") for i in range(n) for j in ["left","right"]]
    for m in range(len(motors)):
        if m < 2:
            motors[m].setVelocity(0.5)
        else:
            motors[m].setVelocity(1.0)
    try:
        assert H >= 0
        theta = asin(H/(L*n))
        x = sqrt(L**2 - H**2/n**2)
        delta_x = (L - x)/2
    except:
        print(f"ERROR - the desired height H is not reachable with the current configuration of the scissor lift.")
    else:
            
        for m in range(len(motors)):
            if m < 2:
                motors[m].setPosition(theta)
            else:
                motors[m].setPosition(2*theta)
        motorT = robot.getDevice('top motor')
        motorT.setVelocity(0.5)
        motorT.setPosition(theta)
        bml = robot.getDevice('base motor left')
        bmr = robot.getDevice('base motor right')
        bml.setVelocity(pi * delta_x/theta)
        bmr.setVelocity(delta_x/theta)
        # bml.setPosition(delta_x)
        bmr.setPosition(-2 * delta_x)



movePlatform(1.5,0.6,4)  

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
