from controller import Robot
from ArmController import ArmController
from NFCReader import NFCReader


class LineFollower():
    def __init__(self, timestep=128):
        #IR sensors
        self.IR = {}
        for name in ["ds_left", "ds_right", "ds_mid"]:
            self.IR[name[3:]] = self.getDevice(name)
            self.IR[name[3:]].enable(timestep)

        self.IR = {}
        for name in ["ds_left", "ds_right", "ds_mid"]:
            self.IR[name[3:]] = self.getDevice(name)
            self.IR[name[3:]].enable(timestep)

        # Initialize wheels
        self.wheels = []
        #Front Left, Back Left, Front Right, Back Right
        wheelsNames = ['wheel_FL', 'wheel_BL', 'wheel_FR', 'wheel_BR']
        for i in range(4):
            self.wheels.append(self.getDevice(wheelsNames[i]))
            self.wheels[i].setPosition(float('inf'))
            self.wheels[i].setVelocity(0.0)
        
    def turn_clockwise(self, speed):
        self.wheels[0].setVelocity(speed)
        self.wheels[1].setVelocity(-speed)
        self.wheels[2].setVelocity(-speed)
        self.wheels[3].setVelocity(speed)


    def turn_until_line_n(self, n):
        pass

    def line_detected(self):
        if self.left <= 900 and self.right<=900 and self.mid>900:
            return True
        else:
            return False
class RobotController(Robot):
    def __init__(self, timestep=128):
        super().__init__()
        self.arm = ArmController(self, timestep=timestep)
        self.nfc_reader = NFCReader(self, timestep=timestep, led_present=False)
        self.nfc_reader.setChannel(-1)

        # Initialize motor
        self.lift_motor = self.getDevice("liftmot")
        self.getDevice("liftpos").enable(timestep)
        
        
        # Initialize Distance Sensors:
        self.left, self.mid, self.right  = self.getDevice("ds_left"), self.getDevice("ds_mid"), self.getDevice("ds_right") 
        self.left.enable(128)
        self.right.enable(128)
        self.mid.enable(128)
        
    def line_tracking(self):
        lf = self.left.getValue()
        rt = self.right.getValue()
        mid = self.mid.getValue()
        leftSpeed = 4
        rightSpeed = 4
        # following white lines
        print(lf, mid, rt)
        
        if lf <= 900 and rt <= 900:
            leftSpeed = 8.0
            rightSpeed = 8.0
        elif lf > 900: #and rt <=900:
            self.strafeLeft(6)
            return None
        elif rt > 900 and lf <=900:
            leftSpeed = 1
            rightSpeed = 5
        
        if mid<=900:
            leftSpeed = leftSpeed/3
            rightSpeed = rightSpeed/3

        print(self.nfc_reader.read())

        self.wheels[0].setVelocity(leftSpeed)
        self.wheels[1].setVelocity(leftSpeed)
        self.wheels[2].setVelocity(rightSpeed)
        self.wheels[3].setVelocity(rightSpeed)

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
