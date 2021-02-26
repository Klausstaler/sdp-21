from controller import Robot
from types import SimpleNamespace
from BasicNavigation import BasicNavigation

class Navigation(BasicNavigation):
    def __init__(self, robot: Robot, timestep=128):
        super().__init__(robot, timestep=128)

    def follow_line(self, speed = 3):
        nearLine = True
        if self.sensors_values(left=[0,0.5], mid=[1], right=[0,0.5]):
            print("case straight")
            self.move_forward(speed*3)
        elif self.sensors_values(left=[0], mid=[0], right=[1]):
            print("strafe right")
            self.strafe(speed, right=True)
        elif self.sensors_values(left=[1], mid=[0], right=[0]):
            print("strafe left")
            self.strafe(speed, right=False)   
        elif self.sensors_values(left=[0], mid=[0,0.5,1], right=[1,0.5]):
            print("turn wheels top right")
            self.turn_on_wheel_axis(speed, left=False, top=True)
        elif self.sensors_values(left=[1,0.5], mid=[0,0.5,1], right=[0]):
            print("turn wheels top left")
            self.turn_on_wheel_axis(speed, left=True, top=True)
        elif self.sensors_values(left=[0], mid=[0], right=[0]):
            print("noneeee")
            nearLine = False
            self.move_forward(speed/2)
        print(self.line_detected())
        return nearLine

    # n=1 is turn until the first line you see, 
    def turn_until_line_n(self, n=1, new=False, speed = 10):
        if new:
            self.n_lines = n
            self.n_line_token = False
        print(self.n_lines, self.line_detected(strong=True))
        if self.n_lines>1:
            self.turn(speed, clock=True)
            if self.line_detected(strong=True) and not self.n_line_token:
                self.n_line_token = True
            elif self.n_line_token == True and not self.line_detected(strong=True):
                self.n_lines-=1
                self.n_line_token = False
            return False
        elif self.n_lines==1:
            self.turn(speed, clock=True)
            if self.line_detected(strong=True):
                self.stop()
                return True
        else:
            self.stop()
            return True

    
    