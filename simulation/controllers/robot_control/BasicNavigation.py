from types import SimpleNamespace

from controller import Robot


class BasicNavigation:
    def __init__(self, robot: Robot, timestep=128):
        self.max_val = 150
        self.low_val = 120
        self.high_val = 140

        # Front distance sensor
        self.ds_front = robot.getDevice('ds_front')
        self.ds_front.enable(timestep)

        #Specifys how far away the bot must be from the object infront of it in order to move forward (in CM)
        self.safety_distance = 100

        #IR sensors
        IR = {}

        for name in ["ds_left", "ds_right", "ds_mid","ds_back"]:
            IR[name[3:]] = robot.getDevice(name)
            IR[name[3:]].enable(timestep)
        self.IR = SimpleNamespace(**IR)

        # Wheels # Front Left, Back Left, Front Right, Back Right
        Wheels = {}
        for name in ['wheel_FL', 'wheel_FR', 'wheel_BL', 'wheel_BR']:
            Wheels[name[6:]] = robot.getDevice(name)
            # self.Wheels[name[6:]].enable(timestep)
            Wheels[name[6:]].setPosition(float('inf'))
            Wheels[name[6:]].setVelocity(0.0)
        self.wheels = SimpleNamespace(**Wheels)


    def sensor_value(self, name, value=None):
        if value is None:
            if name == "left":
                value = self.IR.left.getValue()
            elif name == "right":
                value = self.IR.right.getValue()
            elif name == "mid":
                value = self.IR.mid.getValue()
            elif name == "back":
                value = self.IR.back.getValue()
        if value > 0 and value <= self.low_val:
            return 0
        elif value > self.low_val and value <= self.high_val:
            return 0.5
        elif value > self.high_val:
            return 1

    def sensors_values(self, left, mid, right, back):
        values = [left, mid, right, back]
        ans = True
        for i, name in enumerate(["left", "mid", "right", "back"]):
            ans = ans and (self.sensor_value(name) in values[i])
        return ans

    def get_front_distance_value(self):
        return self.ds_front.getValue()

    def set_wheel_speeds(self, FL, FR, BL, BR):
        self.wheels.FL.setVelocity(FL)
        self.wheels.FR.setVelocity(FR)
        self.wheels.BL.setVelocity(BL)
        self.wheels.BR.setVelocity(BR)

    def wrapper(self, speed, right, clock, top, left):
        pass

    def move_forward(self, speed, right=None, top=None, clock=None):
        self.set_wheel_speeds(speed, speed, speed, speed)

    def move_diagonal(self, speed, right=True, top=None, clock=None):
        if not right:
            self.set_wheel_speeds(speed, -1, -1, speed)
        else:
            self.set_wheel_speeds(-1, speed, speed, -1)

    def stop(self):
        self.set_wheel_speeds(0, 0, 0, 0)

    def strafe(self, speed, right, top=None, clock=None):
        # print(right)
        if not right:
            speed *= -1
        self.set_wheel_speeds(-speed, speed, speed, -speed)

    def turn(self, speed, clock=True, top=None, right=None):
        if not clock:
            speed *= -1
        self.set_wheel_speeds(speed, -speed, speed, -speed)

    def turn_on_wheel_axis(self, speed, right=False, top=True, clock=None):
        if top:
            speed *= -1
        if right:
            self.set_wheel_speeds(0., speed, 0., speed)
        else:
            self.set_wheel_speeds(speed, 0., speed, 0.)

    def line_detected(self, strong=False):
        print("----",self.IR.left.getValue(), self.IR.mid.getValue(),self.IR.right.getValue())
        if self.sensors_values(left=[0,0], mid=[1], right=[0,0], back=[0,0.5,1]):
            return True
        else:
            return False        
        # if strong:
        #     if self.sensors_values(left=[0, 0.5], mid=[1], right=[0, 0.5]):
        #         return True
        #     else:
        #         return False
        # else:
        #     if self.sensors_values(left=[0, 0.5], mid=[1, 0.5], right=[0, 0.5]):
        #         return True
        #     elif self.sensor_value("left") == 1 or self.sensor_value("right") == 1:
        #         return True
        #     else:
        #         return False
