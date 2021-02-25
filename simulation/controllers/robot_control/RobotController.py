from controller import Robot
from ArmController import ArmController
from NFCReader import NFCReader
from types import SimpleNamespace

class Navigation:
    def __init__(self, robot: Robot, timestep=128):
        self.max_val = 150
        self.low_val = 123
        self.high_val = 140
        #IR sensors
        IR = {}
        for name in ["ds_left", "ds_right", "ds_mid"]:
            IR[name[3:]] = robot.getDevice(name)
            IR[name[3:]].enable(timestep)
        self.IR = SimpleNamespace(**IR)

        # Wheels # Front Left, Back Left, Front Right, Back Right
        Wheels = {}
        for name in ['wheel_FL', 'wheel_BL', 'wheel_FR', 'wheel_BR']:
            Wheels[name[6:]] = robot.getDevice(name)
            # self.Wheels[name[6:]].enable(timestep)
            Wheels[name[6:]].setPosition(float('inf'))
            Wheels[name[6:]].setVelocity(0.0)
        self.wheels = SimpleNamespace(**Wheels)

    def sensor_value(self, name, value=None):
        if value is None:
            if name=="left":
                value = self.IR.left.getValue()
            elif name=="right":
                value = self.IR.right.getValue()
            elif name == "mid":
                value = self.IR.mid.getValue()
        if value >0 and value<=self.low_val:
            return 0
        elif value >self.low_val and value<= self.high_val:
            return 0.5
        elif value >self.high_val:
            return 1

    def sensors_values(self, left, mid, right):
        values = [left, mid, right]
        ans = True
        for i, name in enumerate(["left","mid","right"]):
            # print(self.sensor_value(name), values[i], values, ans)
            ans = ans and (self.sensor_value(name) in values[i])
        # print("--"*10)
        return ans

    def set_wheel_speeds(self, FL, FR, BL, BR):
        self.wheels.FL.setVelocity(FL)
        self.wheels.FR.setVelocity(FR)
        self.wheels.BL.setVelocity(BL)
        self.wheels.BR.setVelocity(BR)

    # n=1 is turn until the first line you see, 
    def turn_until_line_n(self, n=1, new=False, speed = 6):
        if new:
            self.n_lines = n
            self.n_line_token = False
        # print(self.n_lines, self.n_line_token)

        if self.n_lines>1:
            self.turn(speed, clock=True)
            if self.line_detected() and not self.n_line_token:
                self.n_line_token = True
            elif self.n_line_token == True and not self.line_detected():
                self.n_lines-=1
                self.n_line_token = False
            return False
        elif self.n_lines==1:
            self.turn(speed, clock=True)
            if self.line_detected():
                self.stop()
                return True
        else:
            self.stop()
            return True

    def follow_line(self, speed = 3):
        nearLine = True

        if self.sensors_values(left=[0,0.5], mid=[1], right=[0,0.5]):
            print("case straight")
            self.move_forward(speed*2)
        elif self.sensors_values(left=[0], mid=[0], right=[1]):
            self.strafe(speed, right=True)
        elif self.sensors_values(left=[1], mid=[0], right=[0]):
            self.strafe(speed, right=False)   
        elif self.sensors_values(left=[0], mid=[0,0.5,1], right=[1]):
            print("case right")
            self.turn_on_wheel_axis(speed, left=False, top=True)
        elif self.sensors_values(left=[1], mid=[0,0.5,1], right=[0]):
            print("case left")
            self.turn_on_wheel_axis(speed, left=True, top=True)
        elif self.sensors_values(left=[0], mid=[0], right=[0]):
            print("noneeee")
            nearLine = False
            self.move_forward(speed/2)
        print(self.line_detected())
        return nearLine

    def move_forward(self, speed):
        self.set_wheel_speeds(speed, speed, speed, speed)

    def stop(self):
        self.set_wheel_speeds(0, 0, 0, 0)

    def strafe(self, speed, right=True):
        if not right:
            speed *=-1
        self.set_wheel_speeds(speed, -speed, -speed, speed)

    def turn(self, speed, clock=True):
        if not clock:
            speed *=-1
        self.set_wheel_speeds(speed, -speed, speed, -speed)
    
    def turn_on_wheel_axis(self, speed, left=True, top=True):
        if top:
            speed*=-1
        if left:
            self.set_wheel_speeds(0.1, speed, 0.1, speed)
        else:
            self.set_wheel_speeds(speed, 0.1, speed, 0.1)
    
    def line_detected(self):
        print("----",self.IR.left.getValue(), self.IR.mid.getValue(),self.IR.right.getValue())
        if self.sensors_values(left=[0,0.5], mid=[1, 0.5], right=[0,0.5]):
            return True
        elif self.sensor_value("left")==1 or self.sensor_value("right")==1:
            return True
        else:
            return False
class RobotController(Robot):
    def __init__(self, timestep=128, params=None):
        super().__init__()
        self.arm = ArmController(self, timestep=timestep)
        self.nfc_reader = NFCReader(self, timestep=timestep, led_present=False)
        self.nfc_reader.setChannel(-1)

        # Initialize Navigation
        self.nav = Navigation(self, timestep=timestep)
        self.nav.turn_until_line_n(n=1, new=True)

        self.follow_line = True
        self.turning = False
        self.reached_node = False
        self.node_to_reach = None

    def reach_node(self, node):
        self.node_to_reach = node
        # self.nav.turn_clockwise(4)
        self.follow_line = self.nav.follow_line()
        # return False
        # if not self.reached_node:
        #     if self.follow_line:
        #         # print("following line")
        #         self.follow_line = self.nav.follow_line()
        #     elif self.turning:
        #         # print("turning")
        #         self.follow_line = self.nav.turn_until_line_n()
        #     else:
        #         self.nav.turn_until_line_n(n=1, new=True)
        #         self.turning = True
        # else:
        #     self.nav.stop()
        # if message:=self.nfc_reader.read():
        #     print(message)
        # if message == self.node_to_reach:
        #     self.reached_node = True
        #     self.nav.stop()
        #     return True
        
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
