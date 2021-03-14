import sys
from typing import Union

import numpy as np
from controller import Robot

try:
    import ikpy
    from ikpy.chain import Chain
    from ikpy.utils import geometry
except ImportError:
    sys.exit('The "ikpy" Python module is not installed. '
             'To run this sample, please upgrade "pip" and install ikpy with this command: "pip install ikpy"')


def convert_rpy(rpy: Union[list, np.array]) -> Union[list, np.array]:
    """
    pretty annoying: webots flips yaw and pitch vs standard convention, also the angle is reversed
    :param rpy: rpy in webots format
    :return: rpy in usual format
    """
    rpy[0], rpy[1], rpy[2] = -rpy[0], -rpy[1], -rpy[2]
    rpy[1], rpy[2] = rpy[2], rpy[1]
    return rpy


INITIAL_PICKUP_X = -.5


class ArmController:

    def __init__(self, robot: Robot, timestep=128):
        # Initialize the arm motors and encoders.
        self.arm_chain = self.get_armchain()
        self.suction_cup = robot.getDevice("robot_box_connector")
        self.suction_cup.enablePresence(timestep)
        self.motors = []

        for link in self.arm_chain.links:
            if any(joint_name in link.name for joint_name in ["arm", "linear_actuator"]):
                motor = robot.getDevice(link.name)
                motor.setVelocity(.4)
                position_sensor = motor.getPositionSensor()
                position_sensor.enable(timestep)
                motor.setPosition(0.0)
                self.motors.append(motor)

        self.pickup_x = INITIAL_PICKUP_X  # used to try different pickup locations if pickup fails

        # Deactivate fixed joints
        for i in [0, 1, 2]:
            self.arm_chain.active_links_mask[i] = False

    def get_armchain(self) -> Chain:
        """
        with tempfile.NamedTemporaryFile(suffix='.urdf', delete=False) as file:
            filename = file.name
            file.write(self.getUrdf().encode('utf-8'))
        """
        """
        with open("robot.urdf","w") as f:
            f.write(self.getUrdf())
        #"""
        arm_chain = Chain.from_urdf_file("../robot_control/robot.urdf")
        return arm_chain

    def move_endeffector(self, coordinate: np.array):
        """
        Moves end-effector to an x,y,z position relative to the base of the arm.
        :param coordinate: The x,y,z coordinate relative to the base of the arm
        :return:
        """
        # 0's for fixed joints, rest of the links have a joint associated with them
        initial_joints = self.get_joint_config()
        ik_results = self.arm_chain.inverse_kinematics(coordinate, target_orientation=np.array([-1, 0, 1]),
                                                       # no idea why this is the correct target_orientation
                                                       orientation_mode="Z",
                                                       max_iter=4,
                                                       initial_position=initial_joints)
        for i, motor in enumerate(self.motors):
            motor.setPosition(ik_results[i + 3])  # ignore first three joints as they are fixed

    def get_joint_config(self) -> list:
        return [0, 0, 0] + [m.getPositionSensor().getValue() for m in self.motors]

    def park_parcel(self):
        parking_location = np.array([-.1, .18, .04])
        self.move_endeffector(parking_location)

    def is_parked(self, parking_location):
        curr_pos = self.arm_chain.forward_kinematics(self.get_joint_config())[:3, 3]
        return round(np.linalg.norm(parking_location - curr_pos), 4) <= 0.05

    def try_pickup(self):
        relative_target = np.array([self.pickup_x, .1678, 0.04])
        self.move_endeffector(relative_target)

        is_present = self.suction_cup.getPresence()
        is_locked = self.suction_cup.isLocked()
        if is_present and not is_locked:
            self.suction_cup.lock()
        if is_locked:
            self.park_parcel()
            if self.is_parked(np.array([-.1, .18, .04])):
                self.pickup_x = INITIAL_PICKUP_X
                return True  # success
        else:
            self.pickup_x -= .01
        return False

    def try_dropoff(self):
        is_present = self.suction_cup.getPresence()
        is_locked = self.suction_cup.isLocked()
        if is_present and is_locked:
            relative_target = np.array([self.pickup_x - 0.15, .1678, 0.04])
            self.move_endeffector(relative_target)
            if self.is_parked(relative_target):
                print("Dropoff Achieved")
                self.suction_cup.unlock()
                self.pickup_x = INITIAL_PICKUP_X
                return True  # success

    def convert_relative(self, global_coord: np.array) -> np.array:
        """
        Converts a global coordinate to a relative coordinate in the frame of the robot.
        :param global_coord: The global coordiante frame
        :return:
        """
        arm_pos = np.array(self.getSelf().getPosition())
        relative_pos = global_coord - arm_pos
        rot_mat = geometry.rpy_matrix(*self.get_rpy())
        relative_pos = rot_mat @ relative_pos
        return relative_pos

    def get_rpy(self) -> Union[list, np.array]:
        return convert_rpy(self.imu.getRollPitchYaw())
