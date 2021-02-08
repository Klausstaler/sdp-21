from controller import Robot, Emitter

robot = Robot()

TIME_STEP = 1

receiver = robot.getDevice("receiver")
receiver.setChannel(0)
# print("what", emitter)
# emitter.enable(TIME_STEP)
receiver.enable(TIME_STEP)

i = 0
while robot.step(TIME_STEP) != -1:

    print("recieved:", receiver.getQueueLength(), "i:",i)
    i+=1
    # message=receiver.getData()
    # print("Whatt")
    # print(message)
    # dataList=struct.unpack("h",message)
    # print(dataList)