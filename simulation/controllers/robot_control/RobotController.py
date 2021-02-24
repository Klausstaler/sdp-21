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

    def follow_line(self,):
        pass
        # if lf <= 900 and rt <= 900:
        #     leftSpeed = 8.0
        #     rightSpeed = 8.0
        # elif lf > 900: #and rt <=900:
        #     self.strafeLeft(6)
        #     return None
        # elif rt > 900 and lf <=900:
        #     leftSpeed = 1
        #     rightSpeed = 5
        
        # if mid<=900:
        #     leftSpeed = leftSpeed/3
        #     rightSpeed = rightSpeed/3

    def turn_clockwise(self, speed):
        self.wheels.FL.setVelocity(-speed)
        self.wheels.FR.setVelocity(speed)
        self.wheels.BL.setVelocity(-speed)
        self.wheels.BR.setVelocity(speed)
        print(self.line_detected())
    

    # n=1 is turn until the first line you see, 
    def turn_until_line_n(self, n):
        token = False
        while n!=0:
            self.turn_clockwise(4)
            if self.line_detected() and token == False:
                token = True
            if token == True and self.line_detected() ==False:
                n-=1
                token = False

    def line_detected(self):
        if self.IR.left.getValue() <= 900 and self.IR.right.getValue()<=900 and self.IR.mid.getValue()>900:
            return True
        else:
            return False
class RobotController(Robot):
    def __init__(self, timestep=128):
        super().__init__()
        self.arm = ArmController(self, timestep=timestep)
        self.nfc_reader = NFCReader(self, timestep=timestep, led_present=False)
        self.nfc_reader.setChannel(-1)

        # Initialize Navigation
        self.nav = Navigation(self, timestep=timestep)

        
        
    def line_tracking(self):
        self.nav.turn_until_line_n(2)
        # lf = self.left.getValue()
        # rt = self.right.getValue()
        # mid = self.mid.getValue()
        # leftSpeed = 4
        # rightSpeed = 4
        # # following white lines
        # print(lf, mid, rt)
        
        # if lf <= 900 and rt <= 900:
        #     leftSpeed = 8.0
        #     rightSpeed = 8.0
        # elif lf > 900: #and rt <=900:
        #     self.strafeLeft(6)
        #     return None
        # elif rt > 900 and lf <=900:
        #     leftSpeed = 1
        #     rightSpeed = 5
        
        # if mid<=900:
        #     leftSpeed = leftSpeed/3
        #     rightSpeed = rightSpeed/3
        if message:=self.nfc_reader.read():
            print(message)
        
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
