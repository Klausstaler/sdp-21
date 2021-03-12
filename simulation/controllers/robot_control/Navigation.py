from controller import Robot

from BasicNavigation import BasicNavigation


class Navigation(BasicNavigation):
    def __init__(self, robot: Robot, timestep=128):
        super().__init__(robot, timestep=128)

    def movment_wrapper(self, func_name, time, total_time, new=False, speed=4, right=False, top=False, clock=False):
        time, speed, total_time = int(time), int(speed), int(total_time)
        right, clock, top = right == "True", clock == "True", top == "True"

        func = getattr(self, func_name)

        if new:
            self.time = time
        if success := time - self.time < total_time:
            func(speed=speed, right=right, top=top, clock=clock)

        # print(time, total_time, self.time, success, right)
        return not success

    def follow_line(self, speed=3.5):
        nearLine = True
        case = "none"
        
        if self.sensors_values(left=[0,0.5,1], mid=[0,0.5,1], right=[0,0.5,1]):
            case = "Lost, keep going"
            self.move_forward(speed)

        if self.sensors_values(left=[0], mid=[1], right=[0]):
            case = "straight"
            self.move_forward(speed * 2)
        elif self.sensors_values(left=[0,0.5], mid=[1], right=[0,0.5]):
            case = "slow straight"
            self.move_forward(speed)
        
        if self.sensors_values(left=[1], mid=[0,0.5], right=[0,0.5]):
            case = "left"
            self.turn(speed, clock=False)

        if self.sensors_values(left=[0,0], mid=[0.5], right=[0.5]):
            case = "right"
            self.turn(speed, clock=True)

        if (self.sensors_values(left=[1], mid=[1], right=[0]) or
            self.sensors_values(left=[0], mid=[1], right=[1])):
            case = "straight, but junction"
            self.move_forward(speed)
        
        


        print("case",case,"----",self.IR.left.getValue(), self.IR.mid.getValue(),self.IR.right.getValue())
        
        # if self.sensors_values(left=[0, 0.5], mid=[1], right=[0, 0.5]):
        #     print("case straight")
        #     self.move_forward(speed * 2)
        # elif self.sensors_values(left=[1], mid=[1], right=[0]) or self.sensors_values(left=[0], mid=[1], right=[1]):
        #     self.move_forward(speed)
        #     print("case straight")
        # elif self.sensors_values(left=[0], mid=[0], right=[1]):
        #     print("strafe right")
        #     self.strafe(speed, right=True)
        # elif self.sensors_values(left=[1], mid=[0], right=[0]):
        #     print("strafe left")
        #     self.strafe(speed, right=False)
        # elif self.sensors_values(left=[0], mid=[0, 0.5, 1], right=[1, 0.5]):
        #     print("turn wheels top right")
        #     self.turn_on_wheel_axis(speed, right=True, top=True)
        # elif self.sensors_values(left=[1, 0.5], mid=[0, 0.5, 1], right=[0]):
        #     print("turn wheels top left")
        #     self.turn_on_wheel_axis(speed, right=False, top=True)
        # elif self.sensors_values(left=[0], mid=[0], right=[0]):
        #     print("noneeee")
        #     # nearLine = False
        #     self.move_forward(speed)
        # else:
        #     print("Doing nothing!")

        # print(self.line_detected())
        return nearLine

    # n=1 is turn until the first line you see, 
    def turn_until_line_n(self, n=1, new=False, speed=5):
        if new:
            self.n_lines = int(n)
            self.n_line_token = False
        # print(self.n_lines, self.line_detected(strong=True))
        if self.n_lines > 1:
            self.turn(speed, clock=True)
            if self.line_detected(strong=True) and not self.n_line_token:
                self.n_line_token = True
            elif self.n_line_token == True and not self.line_detected(strong=True):
                self.n_lines -= 1
                self.n_line_token = False
            return False
        elif self.n_lines == 1:
            self.turn(speed, clock=True)
            if self.line_detected(strong=True):
                self.stop()
                return True
        else:
            self.stop()
            return True
