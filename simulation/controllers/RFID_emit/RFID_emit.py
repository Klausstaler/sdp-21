from controller import LED, Robot, Emitter
import struct
import math

class NFC():
    def __init__(self, robot, name):
        self.__emitter  = robot.getDevice(name)
        robotId    = self.convertToNumber(name)
        self.message    = struct.pack("l", robotId)

    def send(self):
        return self.__emitter.send(self.message)
                  
    def convertToNumber(self, s):
        return int.from_bytes(s.encode(), 'little')

    def setChannel(self, channel=-1):
        if channel==-1: # All channels
            channel = Emitter.CHANNEL_BROADCAST
        else:
            self.__emitter.setChannel(channel)
    
    def setRange(self, range=-1):
        self.__emitter.setRange(range)

    def getRange(self,):
        return self.__emitter.getRange()

    def getChannel(self,):
        return self.__emitter.getChannel()

TIME_STEP = 32

def main():
    robot = Robot()

    nfc = NFC(robot, "emitter")
    nfc.setChannel(0)

    while robot.step(32) != -1:


if __name__ == '__main__':
    main()
    