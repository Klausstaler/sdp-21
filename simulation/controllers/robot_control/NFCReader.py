import math
import struct

from controller import Robot, Receiver


class NFCReader:
    def __init__(self, robot: Robot, timestep=128, led_present=False):
        self.__receiver: Receiver = robot.getDevice("receiver")
        self.__receiver.enable(timestep)
        # self.LED: Union[None, LED] = None
        # if led_present:
        self.LED = robot.getDevice("led")

    def read(self):
        message_str = None

        queue_len = self.__receiver.getQueueLength()
        if queue_len > 0:
            if self.LED:
                self.LED.set(value=1)
            message = self.__receiver.getData()
            size = self.__receiver.getDataSize()
            structure = str(size) + "s"
            data_list = struct.unpack(structure, message)
            message_str = data_list[0].decode()
            self.__receiver.nextPacket()
        else:
            if self.LED:
                self.LED.set(value=0)

        return message_str

    def convertFromNumber(self, n):
        return n.to_bytes(math.ceil(n.bit_length() / 8), 'little').decode()

    def setChannel(self, channel=-1):
        if channel == -1:  # All channels
            channel = Receiver.CHANNEL_BROADCAST
        else:
            self.__receiver.setChannel(channel)

    def getChannel(self, ):
        return self.__receiver.getChannel()
