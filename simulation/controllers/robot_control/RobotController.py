from controller import Robot
from ArmController import ArmController
from NFCReader import NFCReader
from Navigation import Navigation

class TaskCompletion():
    def __init__(self) -> None:
        pass


class RobotController(Robot):
    def __init__(self, timestep=128, params=None):
        super().__init__()
        self.arm = ArmController(self, timestep=timestep)
        self.nfc_reader = NFCReader(self, timestep=timestep, led_present=False)
        self.nfc_reader.setChannel(-1)

        # Initialize Navigation
        self.nav = Navigation(self, timestep=timestep)
        #self.nav.turn_until_line_n(n=1, new=True)

        self.lift_motor = self.getDevice("liftmot")
        self.getDevice("liftpos").enable(timestep)
        self.lift_motor.setPosition(0.0)

        self.follow_line = True
        self.turning = False
        self.turned = False
        self.reached_node = False
        self.node_to_reach = None

    def reach_node(self, node):
        self.turned =False
        self.node_to_reach = node
        # self.nav.follow_line(speed=3)
        if not self.reached_node:
            if self.follow_line:
                # print("following line")
                self.follow_line = self.nav.follow_line()
                self.turning = False
            elif self.turning:
                # print("turning")
                self.follow_line = self.nav.turn_until_line_n()
            else:
                self.nav.turn_until_line_n(n=1, new=True)
                self.turning = True
        else:
            self.nav.stop()

        return self.check_reach_node()

    def turn_until(self, n):
        self.reached_node = False
        if self.turning and not self.turned:
            self.turned = self.nav.turn_until_line_n()
        elif not self.turned:
            self.nav.turn_until_line_n(n=n+1, new=True)
            self.turning = True
        print("have i turned?",self.turned)
        return self.turned


    def check_reach_node(self):
        if message:=self.nfc_reader.read():
            print(message)
        # if message!=None:
        #     # self.nav.stop()
        #     return True
        if message == self.node_to_reach:
            self.reached_node = True
            self.nav.stop()
            return True
        
    def liftUp(self):
        if (self.liftSens.getValue() < self.lift.getMaxPosition()):
            self.lift.setVelocity(1)
        else:
            self.lift.setVelocity(0)

    def liftDown(self):
        if (self.liftSens.getValue() > self.lift.getMinPosition()):
            self.lift.setVelocity(-1)
        else:
            self.lift.setVelocity(0)

    def raise_platform(self, height: str) -> bool:
        height = float(height)
        self.lift_motor.setPosition(height)
        return abs(self.lift_motor.getPositionSensor().getValue() - height) < 0.001
