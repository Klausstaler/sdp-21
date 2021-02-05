from controller import Supervisor
import sys, tempfile
try:
    import ikpy
    from ikpy.chain import Chain
except ImportError:
    sys.exit('The "ikpy" Python module is not installed. '
             'To run this sample, please upgrade "pip" and install ikpy with this command: "pip install ikpy"')

class RobotController(Supervisor):



    def __init__(self, timestep=128):
        # Initialize the arm motors and encoders.
        super().__init__()
        self.arm_chain = self.get_armchain()
        self.motors = []
        self.timestep = timestep
        for link in self.arm_chain.links:
            if any(joint_name in link.name for joint_name in ["arm", "linear_actuator"]):
                motor = self.getDevice(link.name)
                motor.setVelocity(1.0)
                position_sensor = motor.getPositionSensor()
                position_sensor.enable(self.timestep)
                self.motors.append(motor)
        print(self.arm_chain)
        print(len(self.motors))
        #print(self.getUrdf().encode('utf-8'))
        #with open("kuka.urdf", "w") as f:
        #    f.write(self.getUrdf())
    def get_armchain(self):
        filename = None
        with tempfile.NamedTemporaryFile(suffix='.urdf', delete=False) as file:
            filename = file.name
            file.write(self.getUrdf().encode('utf-8'))
        arm_chain = Chain.from_urdf_file(filename)
        return arm_chain
