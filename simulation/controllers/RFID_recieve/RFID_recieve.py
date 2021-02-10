from controller import Robot, Emitter
import struct
from controller import LED

robot = Robot()

TIME_STEP = 32

receiver = robot.getDevice("receiver")
receiver.setChannel(0)

led = robot.getDevice("led")
# led.set(value=1)
# print("what", emitter)
# emitter.enable(TIME_STEP)
receiver.enable(TIME_STEP)

i = 0
while robot.step(TIME_STEP) != -1:
    
    queLen = receiver.getQueueLength()
    if (queLen>0):
        led.set(value=1)
        message=receiver.getData()
        # print(message)
        dataList=struct.unpack("l",message)
        # val = dataList[0].decode("utf-8")
        val = dataList[0] 
        print("message is", val, queLen)
        receiver.nextPacket()
    else:
        led.set(value=0)