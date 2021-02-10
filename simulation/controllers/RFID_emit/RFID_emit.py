from controller import Robot, Emitter
import struct











robot = Robot()

TIME_STEP = 32

emitter = robot.getDevice("emitter")

# All channels
emitter.setChannel(0)

i = 0
while robot.step(32) != -1:
    # print("emitted")

    message = struct.pack("l",i)
    val = emitter.send(message)
    i+=val
    # print("emitted 222", i, val)

    # print(emitter.getChannel())
    # pass
    