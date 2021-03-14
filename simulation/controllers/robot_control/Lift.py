from controller import Robot
from math import asin, sqrt, pi


class Lift:

    def __init__(self, robot, L, n):
        # Set up scissor lift attributes
        self.L = L # Length of a scissor rod
        self.n = n # Number of scissors
        self.robot = robot
        self.motors = [robot.getDevice(f"motor {i+1} {j}") for i in range(n) for j in ["left","right"]]
        for m in range(len(self.motors)):
            if m < 2:
                self.motors[m].setVelocity(0.5)
            else:
                self.motors[m].setVelocity(1.0)

    def raisePlatform(self, height: str):
        height = float(height)
        try:
            assert height >= 0
            theta = asin(height / (self.L * self.n))
            x = sqrt(self.L ** 2 - height ** 2 / self.n ** 2)
            delta_x = (self.L - x)/2
        except Exception as e:
            print(f"ERROR - The desired height {height} is not reachable with the current configuration of the scissor lift")
        else:
            for m in range(len(self.motors)):
                if m < 2:
                    self.motors[m].setPosition(theta)
                else:
                    self.motors[m].setPosition(2*theta)
            motorT = self.robot.getDevice('top motor')
            motorT.setVelocity(0.5)
            motorT.setPosition(theta)
            bml = self.robot.getDevice('base motor left')
            bmr = self.robot.getDevice('base motor right')
            bml.setVelocity(delta_x/theta)
            bmr.setVelocity(delta_x/theta)
            # bml.setPosition(delta_x)
            bmr.setPosition(-2 * delta_x)
            # Wait 2 secs just in case
            # self.robot.step(1280)

    def checkHeight(self,H):
        # NEEDS IMPLEMENTING
        return True