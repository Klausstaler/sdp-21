from controller import Robot

# from ArmController import ArmController
from NFCReader import NFCReader
from Navigation import Navigation
from Lift import Lift

class RobotController(Robot):
    def __init__(self, timestep=128, params=None):
        super().__init__()
        # self.arm = ArmController(self, timestep=timestep)
        self.nfc_reader = NFCReader(self, timestep=timestep, led_present=False)
        self.nfc_reader.setChannel(-1)

        # Initialize Navigation
        self.nav = Navigation(self, timestep=timestep)
        # self.nav.turn_until_line_n(n=1, new=True)

        # Initialise scissor lift with measurements
        self.scissor_lift = Lift(self, 0.6, 4)
        self.scissor_lift.raisePlatform("0.01")

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
        message = self.nfc_reader.read()
        if message:
            pass
            #print(message)
        if message == node_to_reach:
            # self.nav.stop()
            return True

    def time_completion(self, t, new=False):
        if new:
            self.t = t
        return

        return True

    def raise_platform(self, height: str) -> bool:
        self.scissor_lift.raisePlatform(height)
        # return abs(self.lift_motor.getPositionSensor().getValue() - height) < 0.005
        # STILL NEED TO IMPLEMENT POSITION CHECKING
        return self.scissor_lift.checkHeight(height)
