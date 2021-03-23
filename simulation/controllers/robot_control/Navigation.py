from controller import Robot

from BasicNavigation import BasicNavigation
from Lift import Lift


class Navigation(BasicNavigation):
    def __init__(self, robot: Robot, timestep=128):
        super().__init__(robot, timestep=128)

    def movement_wrapper(self, func_name, time, total_time, new=False, speed=4, right=False, top=False, clock=False):
        time, speed, total_time = int(time), int(speed), int(total_time)
        right, clock, top = right == "True", clock == "True", top == "True"

        func = getattr(self, func_name)

        if new:
            self.time = time
        success = time - self.time < total_time
        if success:
            func(speed=speed, right=right, top=top, clock=clock)

        # print(time, total_time, self.time, success, right)
        return not success

    def follow_line(self, speed=3.5):
        nearLine = True
        distance_sensor_reading = self.get_front_distance_value()
        #Check for if something is within the bots "safety distance" if so stops
        if(distance_sensor_reading <= self.safety_distance):
            print("Object within safety distance pausing movement (Distance from object {})".format(distance_sensor_reading))
            self.move_forward(0)
            return nearLine

        case = "none"

        if self.sensors_values(left=[0, 0.5, 1], mid=[0, 0.5, 1], right=[0, 0.5, 1]):
            case = "Lost, keep going"
            self.move_forward(speed)

        if self.sensors_values(left=[0], mid=[1], right=[0]):
            case = "straight"
            self.move_forward(speed * 2)
        elif self.sensors_values(left=[0.5], mid=[0.5], right=[0]):
            case = "slow diagonal left"
            self.move_diagonal(speed, right=False)
            self.turn(speed, clock=False)

        elif self.sensors_values(left=[0], mid=[0.5], right=[0.5]):
            case = "slow diagonal right"
            self.move_diagonal(speed, right=True)
            self.turn(speed, clock=True)

        else:
            case = "slow straight"
            self.move_forward(speed)

        if self.sensors_values(left=[1], mid=[0, 0.5], right=[0, 0.5]):
            case = "left"
            self.turn(speed, clock=False)

        if self.sensors_values(left=[0, 0.5], mid=[0, 0.5], right=[1]):
            case = "right"
            self.turn(speed, clock=True)

        if (self.sensors_values(left=[1], mid=[1], right=[0]) or
                self.sensors_values(left=[0], mid=[1], right=[1])):
            case = "straight, but junction"
            self.move_forward(speed)

        # print("case", case, "----", self.IR.left.getValue(), self.IR.mid.getValue(), self.IR.right.getValue())

        return nearLine

    # n=1 is turn until the first line you see, 
    def turn_until_line_n(self, n=1, new=False, speed=10):
        if new:
            self.n_lines = int(n)
            self.n_line_token = False
        print(self.n_lines, self.line_detected(strong=True))
        if self.n_lines > 1:
            self.turn(speed, clock=True)
            if self.line_detected(strong=True) and not self.n_line_token:
                self.n_line_token = True
            elif self.n_line_token and not self.line_detected(strong=True):
                self.n_lines -= 1
                self.n_line_token = False
            return False
        elif self.n_lines == 1:
            self.turn(speed, clock=True)
            if self.line_detected(strong=True):
                print("Yeet")
                self.stop()
                return True
        else:
            print("no line left")
            self.stop()
            return True
