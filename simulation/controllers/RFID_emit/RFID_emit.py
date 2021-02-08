from controller import Robot, Emitter
import struct

robot = Robot()

TIME_STEP = 32

emitter = robot.getDevice("emitter")

# All channels
emitter.setChannel(0)

# print("what", emitter)
# emitter.enable(TIME_STEP)
i = 0
while robot.step(32) != -1:
    message = struct.pack("5s",b"abcde")
    val = emitter.send(message)
    print("emitted", val, i)
    i+=1
    # print(emitter.getChannel())
    # pass
    