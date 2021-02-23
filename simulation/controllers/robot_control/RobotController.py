from controller import Robot
#from ArmController import ArmController
from NFCReader import NFCReader

class RobotController(Robot):
    def __init__(self, timestep=128):
        super().__init__()
        #self.arm = ArmController(self)
        self.nfc_reader = NFCReader(self, timestep=timestep, led_present=False)
        self.nfc_reader.setChannel(0)

        # Initialize motor
        self.lift_motor = self.getDevice("liftmot")
        self.getDevice("liftpos").enable(timestep)
        # Initialize wheels
        self.wheels = []
        self.ds = []
        wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
        dsNames = ['ds_left', 'ds_right']
        for i in range(2):
            self.ds.append(self.getDevice(dsNames[i]))
            self.ds[i].enable(128)
        for i in range(4):
            self.wheels.append(self.getDevice(wheelsNames[i]))
            self.wheels[i].setPosition(float('inf'))
            self.wheels[i].setVelocity(0.0)
    
    def line_tracking(self):
        lf = self.ds[0].getValue()
        rt = self.ds[1].getValue()
        leftSpeed = 8.0
        rightSpeed = 8.0
        # following white lines
        if lf <= 500 and rt <= 500:
            leftSpeed = 8.0
            rightSpeed = 8.0
        elif lf > 500:
            leftSpeed = 4.0
            rightSpeed = 1.5
        elif rt > 500:
            leftSpeed = 1.5
            rightSpeed = 4.0
  
       # if ds[4].getValue() <= 500 or ds[5].getValue() <= 500:
       #     leftSpeed = 0
       #     rightSpeed = 0
        

                
        self.wheels[0].setVelocity(leftSpeed)
        self.wheels[1].setVelocity(leftSpeed)
        self.wheels[2].setVelocity(rightSpeed)
        self.wheels[3].setVelocity(rightSpeed)
    
    
    
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
        self.wheels[1].setVelocity(-speed)
        self.wheels[2].setVelocity(speed)
        self.wheels[3].setVelocity(speed)
        
    def strafeRight(self, speed):
        self.wheels[0].setVelocity(speed)
        self.wheels[1].setVelocity(speed)
        self.wheels[2].setVelocity(-speed)
        self.wheels[3].setVelocity(-speed)

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
   