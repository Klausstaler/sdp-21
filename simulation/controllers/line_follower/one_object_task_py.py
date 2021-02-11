from controller import Robot

TIME_STEP = 64
robot = Robot()

ds = []
dsNames = ['ds_left', 'ds_right', 'ds_top_left', 'ds_top_right', 'ds_left_intersect', 'ds_right_intersect']
for i in range(6):
    ds.append(robot.getDevice(dsNames[i]))
    ds[i].enable(TIME_STEP)
    
wheels = []
wheelsNames = ['motor1', 'motor2', 'motor3', 'motor4']
for i in range(4):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)
avoidObstacleCounter = 0

leftSpeed = 3.0
rightSpeed = 3.0

while robot.step(TIME_STEP) != -1:
    lf_wheel = ds[0].getValue()
    rt_wheel = ds[1].getValue()
    
    # following white lines
    ## ideally less than 500 for white line 
    if lf_wheel <= 500 and rt_wheel <= 500:
        leftSpeed = 3.0
        rightSpeed = 3.0
    elif lf_wheel > 500:
        leftSpeed = 4.0
        rightSpeed = 1.5
    elif rt_wheel > 500:
        leftSpeed = 1.5
        rightSpeed = 4.0
    
    if ds[4].getValue() <= 500 or ds[5].getValue() <= 500:
        leftSpeed = 0
        rightSpeed = 0
    
    # avoid collisions
    if avoidObstacleCounter > 0:
        avoidObstacleCounter -= 1
        leftSpeed = 1.0
        rightSpeed = -1.0
    else:  # read sensors
        for i in range(2):
            if ds[i+2].getValue() < 950.0:
                avoidObstacleCounter = 20
                
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    wheels[2].setVelocity(leftSpeed)
    wheels[3].setVelocity(rightSpeed)