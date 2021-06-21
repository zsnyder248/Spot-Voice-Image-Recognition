#Stephen Bowen 2021
#System modules
import time

# Boston Dynamics modules
from bosdyn.api.spot import robot_command_pb2 as spot_command_pb2
from bosdyn.client.estop import EstopEndpoint, EstopKeepAlive, EstopClient
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient, blocking_stand
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive
import bosdyn.client.util


#Custom modules
from Estop import Estop

VELOCITY_BASE_SPEED = 2.0  # m/s
VELOCITY_BASE_ANGULAR = 0.8  # rad/sec
VELOCITY_CMD_DURATION = 0.6  # seconds

class Spot():

    def __init__(self, username, password, spotIP):
        # Gather and assign credntials and Spot's IP
        self.__username = username
        self.__password = password
        self.spotIP = spotIP
        
        # Set power state for Spot
        self._isPoweredOn = False

    # Authenticate user and build required interfaces
    def auth(self):
        try:
            # Create robot object
            sdk = bosdyn.client.create_standard_sdk('Dug')
            self._robot = sdk.create_robot(self.spotIP)
            self._robot.authenticate(self.__username, self.__password)

            # Create estop client for the robot
            estop_client = self._robot.ensure_client(EstopClient.default_service_name)

            # Create estop endpoint
            self.estop = Estop(estop_client, 60, 'Dug estop')

            # Create robot state, command, and lease clients
            self._state_client = self._robot.ensure_client(RobotStateClient.default_service_name)

            self._robot_command_client = self._robot.ensure_client(RobotCommandClient.default_service_name)
            self._lease_client = self._robot.ensure_client(LeaseClient.default_service_name)

            # Acquire and retain lease and robot id
            self._lease = self._lease_client.acquire()

            # Construct our lease keep-alive object, which begins RetainLease calls in a thread.
            self._lease_keepalive = LeaseKeepAlive(self._lease_client)
            self._robot_id = self._robot.get_id()
            
            return True
        except:
            print("EXCEPTION")
            return False

    # Power Spot on/off
    def togglePower(self):
        try:
            if self._isPoweredOn:
                self._robot.power_off()
                self._isPoweredOn = False
            else:
                self._robot.power_on()
                self._isPoweredOn = True
            return self._isPoweredOn
        except:
            return self._isPoweredOn

    # Trigger EStop
    def eStop(self):
        self.estop.stop()
        print("STOPPING")

    # Clear EStop
    def clearEStop(self):
        status = self.estop.allow()
        try: 
            self._robot.power_on()
            return status
        except:
            return status

    # End connection to robot
    def endConnection(self):
        # Return lease and end Estop coverage
        self._lease_client.return_lease(self._lease)
        self._lease_keepalive.shutdown()
        self._lease_keepalive = None
        self.estop.estop_keep_alive.shutdown()
        return True

    def forward(self):
        moveCommand = RobotCommandBuilder.synchro_velocity_command(v_x=VELOCITY_BASE_SPEED, v_y=0, v_rot=0)
        try:
            self._robot_command_client.robot_command_async(command=moveCommand,end_time_secs=time.time()+VELOCITY_CMD_DURATION)
            return True
        except:
            return False

    def backward(self):
        moveCommand = RobotCommandBuilder.synchro_velocity_command(v_x=-VELOCITY_BASE_SPEED, v_y=0, v_rot=0)
        try:
            self._robot_command_client.robot_command_async(command=moveCommand,end_time_secs=time.time()+VELOCITY_CMD_DURATION)
            return True
        except:
            return False

    def moveRight(self):
        moveCommand = RobotCommandBuilder.synchro_velocity_command(v_x=0, v_y=-VELOCITY_BASE_SPEED, v_rot=0)
        try:
            self._robot_command_client.robot_command_async(command=moveCommand,end_time_secs=time.time()+VELOCITY_CMD_DURATION)
            return True
        except:
            return False

    def turnRight(self):
        moveCommand = RobotCommandBuilder.synchro_velocity_command(v_x=0,v_y=0,v_rot=-VELOCITY_BASE_ANGULAR)
        try:
            self._robot_command_client.robot_command_async(command=moveCommand,end_time_secs=time.time()+VELOCITY_CMD_DURATION)
            return True
        except:
            return False

    def moveLeft(self):
        moveCommand = RobotCommandBuilder.synchro_velocity_command(v_x=0, v_y=VELOCITY_BASE_SPEED, v_rot=0)
        try:
            self._robot_command_client.robot_command_async(command=moveCommand,end_time_secs=time.time()+VELOCITY_CMD_DURATION)
            return True
        except:
            return False

    def turnLeft(self):
        moveCommand = RobotCommandBuilder.synchro_velocity_command(v_x=0,v_y=0,v_rot=VELOCITY_BASE_ANGULAR)
        try:
            self._robot_command_client.robot_command_async(command=moveCommand,end_time_secs=time.time()+VELOCITY_CMD_DURATION)
            return True
        except:
            return False

    def sit(self):
        moveCommand = RobotCommandBuilder.synchro_sit_command(params=spot_command_pb2.MobilityParams(locomotion_hint=spot_command_pb2.HINT_AUTO, stair_hint=0))
        try:
            self._robot_command_client.robot_command_async(command=moveCommand,end_time_secs=time.time()+VELOCITY_CMD_DURATION)
            return True
        except:
            return False

    def stand(self):
        moveCommand = RobotCommandBuilder.synchro_stand_command(params=spot_command_pb2.MobilityParams(locomotion_hint=spot_command_pb2.HINT_AUTO, stair_hint=0))
        try:
            self._robot_command_client.robot_command_async(command=moveCommand,end_time_secs=time.time()+VELOCITY_CMD_DURATION)
            return True
        except:
            return False