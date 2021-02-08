from controller import Robot, Emitter

robot = Robot()

TIME_STEP = 32

receiver = robot.getDevice("receiver")
receiver.enable(TIME_STEP)
# print("what", emitter)
# emitter.enable(TIME_STEP)

while robot.step(TIME_STEP) != -1:
    # print("WHATT!")
    message=receiver.getData()
    print("Whatt")
    print(message)
    dataList=struct.unpack("h",message)
    print(dataList)