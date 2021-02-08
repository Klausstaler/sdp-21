from controller import Robot, Emitter

robot = Robot()

TIME_STEP = 32

reciever = robot.getDevice("receiver")
reciever.enable(TIME_STEP)
# print("what", emitter)
# emitter.enable(TIME_STEP)

while robot.step(TIME_STEP) != -1:
    print("WHATT!")
    print(reciever.getSamplingPeriod())