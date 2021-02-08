from controller import Robot, Emitter
import struct

robot = Robot()

TIME_STEP = 32

emitter = robot.getDevice("emitter")

# All channels
emitter.setChannel(Emitter.CHANNEL_BROADCAST)

# print("what", emitter)
# emitter.enable(TIME_STEP)
message = struct.pack("h",2)
emitter.send(message)
# while robot.step(32) != -1:
    # print("Not Hello World!")
    # print(emitter.getChannel())
    # pass
    