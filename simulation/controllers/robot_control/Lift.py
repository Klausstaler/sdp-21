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

    def raisePlatform(self, H):
        try:
            assert H >= 0
            theta = asin(H/(self.L*self.n))
            x = sqrt(self.L**2 - H**2/self.n**2)
            delta_x = (self.L - x)/2
        except:
            print(f"ERROR - The desired height {H} is not reachable with the current configuration of the scissor lift")
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
            bml.setVelocity(pi * delta_x/theta)
            bmr.setVelocity(pi * delta_x/theta)
            # bml.setPosition(delta_x)
            bmr.setPosition(-2 * delta_x)

    def checkHeight(self,H):
        # NEEDS IMPLEMENTING
        return True