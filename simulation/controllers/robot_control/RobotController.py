from controller import Robot

from ArmController import ArmController
from NFCReader import NFCReader
from Navigation import Navigation


class RobotController(Robot):
    def __init__(self, timestep=128, params=None):
        super().__init__()
        self.arm = ArmController(self, timestep=timestep)
        self.nfc_reader = NFCReader(self, timestep=timestep, led_present=False)
        self.nfc_reader.setChannel(-1)

        # Initialize Navigation
        self.nav = Navigation(self, timestep=timestep)
        # self.nav.turn_until_line_n(n=1, new=True)

        self.lift_motor = self.getDevice("liftmot")
        self.getDevice("liftpos").enable(timestep)
        self.lift_motor.setPosition(0.0)

        self.follow_line = True
        self.turning = False
        self.t = 0

    def reach_node(self, node):
        # print(self.follow_line, self.turning)
        if self.follow_line:
            self.follow_line = self.nav.follow_line()
            self.turning = False
        elif self.turning:
            self.follow_line = self.nav.turn_until_line_n()
        else:
            self.nav.turn_until_line_n(n=1, new=True)
            self.turning = True
        return node

    def check_reach_node(self, node_to_reach):
        if message := self.nfc_reader.read():
            pass
            #print(message)
        if message == node_to_reach:
            self.nav.stop()
            return True

    def time_completion(self, t, new=False):
        if new:
            self.t = t
        return

        return True

    def raise_platform(self, height: str) -> bool:
        height = float(height)
        self.lift_motor.setPosition(height)
        return abs(self.lift_motor.getPositionSensor().getValue() - height) < 0.005
