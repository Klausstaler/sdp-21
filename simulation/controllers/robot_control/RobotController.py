from controller import Robot
from ArmController import ArmController
from NFCReader import NFCReader
from types import SimpleNamespace

class Navigation:
    def __init__(self, robot: Robot, timestep=128):
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

    # n=1 is turn until the first line you see, 
    def turn_until_line_n(self, n=1, new=False, speed = 4):
        if new:
            self.n_lines = n
            self.n_line_token = False
        # print(self.n_lines, self.n_line_token)

        if self.n_lines>1:
            self.turn_clockwise(speed)
            if self.line_detected() and not self.n_line_token:
                self.n_line_token = True
            elif self.n_line_token == True and not self.line_detected():
                self.n_lines-=1
                self.n_line_token = False
            return False
        elif self.n_lines==1:
            self.turn_clockwise(speed)
            if self.line_detected():
                self.stop()
                return True
        else:
            self.stop()
            return True

    def follow_line(self, speed = 4):
        leftSpeed = speed
        rightSpeed = speed
        turnfactor = 10
        nearLine = True
        # if True:
        # print(self.IR.left.getValue(),self.IR.mid.getValue(),self.IR.right.getValue())

        if self.IR.left.getValue() <= 900 and self.IR.right.getValue()<=900 and self.IR.mid.getValue()>900:
            leftSpeed = speed*2
            rightSpeed = speed*2
        elif self.IR.left.getValue() >= 900 and self.IR.right.getValue()<=900:
            leftSpeed = speed
            rightSpeed = speed/turnfactor
        elif self.IR.left.getValue() <= 900 and self.IR.right.getValue()>=900:
            leftSpeed = speed/turnfactor
            rightSpeed = speed
        # elif self.IR.left.getValue() >= 990 and self.IR.right.getValue()>=990 and self.IR.mid.getValue()>990:
        #     # print("Junction")
        #     leftSpeed = 0
        #     rightSpeed = 0
        #     nearLine = False
        else:
            # print("abababa")
            nearLine = False

        self.wheels.FL.setVelocity(leftSpeed)
        self.wheels.FR.setVelocity(rightSpeed)
        self.wheels.BL.setVelocity(rightSpeed)
        self.wheels.BR.setVelocity(leftSpeed)
        
        return nearLine

    def turn_clockwise(self, speed):
        self.wheels.FL.setVelocity(-speed)
        self.wheels.FR.setVelocity(speed)
        self.wheels.BL.setVelocity(-speed)
        self.wheels.BR.setVelocity(speed)
        print(self.line_detected())
    
    def stop(self):
        self.wheels.FL.setVelocity(0)
        self.wheels.FR.setVelocity(0)
        self.wheels.BL.setVelocity(0)
        self.wheels.BR.setVelocity(0)
        # print(self.line_detected())
    

    def line_detected(self):
        print(self.IR.left.getValue(),self.IR.mid.getValue(),self.IR.right.getValue())
        if self.IR.left.getValue() <= 900 and self.IR.right.getValue()<=900 and self.IR.mid.getValue()>900:
            return True
        elif self.IR.left.getValue() >= 990 or self.IR.right.getValue()>=990 or self.IR.mid.getValue()>=990:
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
        self.nav.turn_clockwise(20)
        return False
        if not self.reached_node:
            if self.follow_line:
                # print("following line")
                self.follow_line = self.nav.follow_line()
            elif self.turning:
                # print("turning")
                self.follow_line = self.nav.turn_until_line_n()
            else:
                self.nav.turn_until_line_n(n=1, new=True)
                self.turning = True
        else:
            self.nav.stop()
        if message:=self.nfc_reader.read():
            print(message)
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
