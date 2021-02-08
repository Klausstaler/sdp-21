from controller import Robot, Emitter

robot = Robot()

TIME_STEP = 32

emitter = robot.getDevice("emitter")

# print("what", emitter)
# emitter.enable(TIME_STEP)

while robot.step(32) != -1:
    print("Not Hello World!")
    print(emitter.getRange())