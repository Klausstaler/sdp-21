from controller import LED, Robot, Emitter
import struct
import math

TIME_STEP = 32

class NFC():
    def __init__(self, robot, name, message=None):
        self.__emitter  = robot.getDevice(name)
        if message is None:
            message = name
        self.packMessage(message)
        
    def packMessage(self, s):
        structure = str(len(s))+"s"
        self.message = struct.pack(structure, s.encode('utf-8'))

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

def main():
    robot = Robot()
    message = robot.getName()
    nfc = NFC(robot, "emitter", message = message)
    nfc.setChannel(0)

    while robot.step(32) != -1:
        nfc.send()

if __name__ == '__main__':
    main()
    