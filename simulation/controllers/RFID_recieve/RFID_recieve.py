from controller import Robot, Emitter
import struct
robot = Robot()

TIME_STEP = 1

receiver = robot.getDevice("receiver")
receiver.setChannel(0)
# print("what", emitter)
# emitter.enable(TIME_STEP)
receiver.enable(TIME_STEP)

i = 0
while robot.step(TIME_STEP) != -1:

    queLen = receiver.getQueueLength()
    if (queLen>0):
        message=receiver.getData()
        # print(message)
        dataList=struct.unpack("5s",message)
        val = dataList[0].decode("utf-8") 
        print("message is", val)