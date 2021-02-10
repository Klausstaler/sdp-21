from controller import Robot, Receiver
import struct
from controller import LED
import math

TIME_STEP = 32

class NFC_reader():
    def __init__(self, robot, LED_present=False):
        self.__receiver = robot.getDevice("receiver")
        self.__receiver.enable(TIME_STEP)

        if LED_present:
            self.LED = robot.getDevice("led")

    def read(self):
        message_str = None

        queLen = self.__receiver.getQueueLength()
        if (queLen>0):
            self.LED.set(value=1)
            message=self.__receiver.getData()
            size = self.__receiver.getDataSize()
            strucutre = str(size)+"s"
            dataList=struct.unpack(strucutre, message)
            message_str = dataList[0].decode()
            self.__receiver.nextPacket()
        else:
            self.LED.set(value=0)
        
        return message_str
    
    def convertFromNumber(self, n):
        return n.to_bytes(math.ceil(n.bit_length() / 8), 'little').decode()

    def setChannel(self, channel=-1):
        if channel==-1: # All channels
            channel = Receiver.CHANNEL_BROADCAST
        else:
            self.__receiver.setChannel(channel)
    
    def getChannel(self,):
        return self.__receiver.getChannel()

def main():
    robot = Robot()
    nfc_reader = NFC_reader(robot, LED_present=True)
    nfc_reader.setChannel(0)
    
    while robot.step(TIME_STEP) != -1:
        message = nfc_reader.read()
        if message is not None:
            print("The message is: ", message)

if __name__ == '__main__':
    main()