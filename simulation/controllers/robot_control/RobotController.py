from controller import Robot
from ArmController import ArmController
from NFCReader import NFCReader


class RobotController(Robot):
    def __init__(self, timestep=128):
        super().__init__()
        self.arm = ArmController(self, timestep=timestep)
        self.nfc_reader = NFCReader(self, timestep=timestep, led_present=False)
        self.nfc_reader.setChannel(0)

        # Initialize motor
        self.lift_motor = self.getDevice("liftmot")
        self.getDevice("liftpos").enable(timestep)
        # Initialize wheels
        self.wheels = []
        wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
        for i in range(4):
            self.wheels.append(self.getDevice(wheelsNames[i]))
            self.wheels[i].setPosition(float('inf'))
            self.wheels[i].setVelocity(0.0)

    def strafeForward(self, speed):
        self.wheels[0].setVelocity(speed)
        self.wheels[1].setVelocity(speed)
        self.wheels[2].setVelocity(speed)
        self.wheels[3].setVelocity(speed)

    def strafeBack(self, speed):
        self.wheels[0].setVelocity(-speed)
        self.wheels[1].setVelocity(-speed)
        self.wheels[2].setVelocity(-speed)
        self.wheels[3].setVelocity(-speed)

    def strafeLeft(self, speed):
        self.wheels[0].setVelocity(-speed)
        self.wheels[1].setVelocity(speed)
        self.wheels[2].setVelocity(speed)
        self.wheels[3].setVelocity(-speed)

    def strafeRight(self, speed):
        self.wheels[0].setVelocity(speed)
        self.wheels[1].setVelocity(-speed)
        self.wheels[2].setVelocity(-speed)
        self.wheels[3].setVelocity(speed)

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
