"""level1 controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from math import asin, sqrt, pi
from types import SimpleNamespace

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())
Wheels = {}
for name in ['wheel_FL', 'wheel_FR', 'wheel_BL', 'wheel_BR']:
    Wheels[name[6:]] = robot.getDevice(name)
    # self.Wheels[name[6:]].enable(timestep)
    Wheels[name[6:]].setPosition(float('inf'))
    Wheels[name[6:]].setVelocity(0.0)
wheels = SimpleNamespace(**Wheels)


def set_wheel_speeds(FL, FR, BL, BR):
    wheels.FL.setVelocity(FL)
    wheels.FR.setVelocity(FR)
    wheels.BL.setVelocity(BL)
    wheels.BR.setVelocity(BR)
    
def set_pos(FL, FR, BL, BR):
    wheels.FL.setPosition(FL)
    wheels.FR.setPosition(FR)
    wheels.BL.setPosition(BL)
    wheels.BR.setPosition(BR)
    
    
def move_forward(speed, distance, right=None, top=None, clock=None):
    set_wheel_speeds(speed, speed, speed, speed)
    set_pos(distance,distance,distance,distance)
    

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



movePlatform(0.5,0.6,4)
robot.step(2000)
move_forward(5.0,30)  

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
