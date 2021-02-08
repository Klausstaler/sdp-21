from controller import Supervisor
import numpy as np
import sys, tempfile
from typing import Union
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



class RobotController(Supervisor):



    def __init__(self, timestep=128):
        # Initialize the arm motors and encoders.
        super().__init__()
        self.arm_chain = self.get_armchain()
        self.imu, self.suction_cup = self.getDevice("robot_imu"), self.getDevice("robot_box_connector")
        self.imu.enable(timestep)
        self.suction_cup.enablePresence(timestep)
        self.motors = []

        for link in self.arm_chain.links:
            if any(joint_name in link.name for joint_name in ["arm", "linear_actuator"]):
                motor = self.getDevice(link.name)
                motor.setVelocity(.4)
                position_sensor = motor.getPositionSensor()
                position_sensor.enable(timestep)
                self.motors.append(motor)

        # Deactivate fixed joints
        for i in [0, 1]:
            self.arm_chain.active_links_mask[i] = False

    def get_armchain(self) -> Chain:
        filename = None
        with tempfile.NamedTemporaryFile(suffix='.urdf', delete=False) as file:
            filename = file.name
            file.write(self.getUrdf().encode('utf-8'))
        arm_chain = Chain.from_urdf_file(filename)
        return arm_chain

    def move_endeffector(self, coordinate: np.array):
        """
        Moves end-effector to an x,y,z position relative to the base of the arm.
        :param coordinate: The x,y,z coordinate relative to the base of the arm
        :return:
        """
        # 0's for fixed joints, rest of the links have a joint associated with them
        initial_joints = self.get_joint_config()
        ik_results = self.arm_chain.inverse_kinematics(coordinate, target_orientation=np.array([-1, 0, 1]), # no idea why this is the correct target_orientation
                                                                   orientation_mode="Z",
                                                                   max_iter=4,
                                                                   initial_position=initial_joints)

        for i, motor in enumerate(self.motors):
            motor.setPosition(ik_results[i+2]) # ignore first two joints as it does not have an associated motor


    def get_joint_config(self) -> list:
        return [0, 0] + [m.getPositionSensor().getValue() for m in self.motors]

    def park_parcel(self):
        parking_location = np.array([-.1, .1678, .04])
        self.move_endeffector(parking_location)

    def try_pickup(self, x_pos):
        relative_target = np.array([x_pos, .1678, 0.04])
        self.move_endeffector(relative_target)
        curr_pos = self.arm_chain.forward_kinematics(self.get_joint_config())[:3, 3]
        if np.linalg.norm(relative_target - curr_pos) < 0.045: # if we are close to the target location but still had no pickup, move forward for pickup
            x_pos -= .01
        return x_pos

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


