from controller import Robot
from types import SimpleNamespace
from BasicNavigation import BasicNavigation

class Navigation(BasicNavigation):
    def __init__(self, robot: Robot, timestep=128):
        super(Navigation, self).__init__()

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

    # n=1 is turn until the first line you see, 
    def turn_until_line_n(self, n=1, new=False, speed = 6):
        if new:
            self.n_lines = n
            self.n_line_token = False
        
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

    
    