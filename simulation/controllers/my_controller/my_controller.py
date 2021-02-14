"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, PositionSensor

class MyController(Robot):
    def __init__(self):
        super(MyController, self).__init__()
        self.timestep = 32       
        self.count = 0
        
        # Initialize wheels
        self.wheels = []
        wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
        for i in range(4):
            self.wheels.append(self.getDevice(wheelsNames[i]))
            self.wheels[i].setPosition(float('inf'))
            self.wheels[i].setVelocity(0.0)
        
        # Initialize lift
        self.lift = self.getDevice('liftmot')
        self.lift.setPosition(float('inf'))
        self.lift.setVelocity(0.0)
        self.liftSens = self.getDevice('liftpos')
        self.liftSens.enable(self.timestep)
        
        
    def run(self):
        while self.step(self.timestep) != -1:
            """"
            speed = 5 # rad/s
            
            countmax = 70
            if(self.count < countmax):
                self.count = self.count + 1
            else:
                self.count = countmax * - 1
                        
            if(self.count < 0):
                self.strafeForward(speed)
                self.liftDown()
            else:
                self.strafeLeft(speed)
                self.liftUp()
            """
            
# Movement functions

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
        if(self.liftSens.getValue() < self.lift.getMaxPosition()):
            self.lift.setVelocity(1)
        else:
            self.lift.setVelocity(0)
    
    def liftDown(self):
        if(self.liftSens.getValue() > self.lift.getMinPosition()):
            self.lift.setVelocity(-1)
        else:
            self.lift.setVelocity(0)
        
        
controller = MyController()
controller.run()
    