import Estop
import sys

def main(argv):
    isPoweredOn = False
    robot = initializeSpot(argv)
    if(robot == False):
        print("Error while initializing Spot. Exiting...")
        sys.exit()

    print("Spot command.\n")

    while(True):
        command = str(input("Enter a command (commands must start with spot) or enter 'end' to stop commanding spot: "))
        print("\n")

        command = command.lower()

        if(command == "stop" or command == "estop"):
            spotEstop()
            break
        elif(command == "end"):
            spotShutdown(robot)
            break
        elif(command == "power"):
            isPoweredOn = togglePower(robot, isPoweredOn)
        elif "spot" not in command:
            print("Command does not begin with spot. Spot doesn't know you're talking to him.\n")
        else:
            selectCommand(command, robot, isPoweredOn)

def initializeSpot(argv):
    username = str(sys.argv[1])
    password = str(sys.argv[2])
    hostname = str(sys.argv[3])
    
    try:
        # Create robot object
        sdk = bosdyn.client.create_standard_sdk('Spot Voice Recognition')
        robot = sdk.create_robot(hostname)
        robot.authenticate(username, password)

        # Create estop client for the robot
        estop_client = robot.ensure_client(EstopClient.default_service_name)

        # Create estop endpoint
        estop = Estop(estop_client, 60, 'Estop')

        # Create robot state, command, and lease clients
        state_client = robot.ensure_client(RobotStateClient.default_service_name)
        command_client = robot.ensure_client(RobotCommandClient.default_service_name)
        lease_client = robot.ensure_client(LeaseClient.default_service_name)

        
        # Construct our lease keep-alive object, which begins RetainLease calls in a thread.
        lease_keepalive = LeaseKeepAlive(lease_client)

        # Acquire and retain lease and robot id
        lease = lease_client.acquire()
        
        return robot
    except:
        return False

def togglePower(robot, isPoweredOn):
    try:
        if(isPoweredOn):
            robot.power_off()
            isPoweredOn = False
        else:
            robot.power_on()
            isPoweredOn = True
        return isPoweredOn
    except:
        return isPoweredOn

def spotEstop():
    print("Spot EMERGENCY stop\n")

def spotShutdown(robot):
    print("Spot shutdown\n")
    robot.lease_client.return_lease(robot.lease)
    robot.lease_keepalive.shutdown()
    robot.lease_keepalive = None
    robot.estop.estop_keep_alive.shutdown()

def selectCommand(command, robot, isPoweredOn):
    command = command.replace("spot ", "")
    print("Command: " + command + "\n")
    if "forward" in command:
        spotForward(robot)
    elif "backward" in command:
        spotBackward(robot)
    elif "right" in command:
        spotRight(robot)
    elif "left" in command:
        spotLeft(robot)
    elif "sit" in command:
        spotSit(robot)
    elif "stand" in command:
        spotStand(robot)

def spotForward(robot):
    print("Spot moving forward\n")

def spotBackward(robot):
    print("Spot moving backward\n")

def spotRight(robot):
    print("Spot turning left\n")

def spotLeft(robot):
    print("Spot turning right\n")

def spotSit(robot):
    print("Spot sitting\n")

def spotStand(robot):
    print("Spot standing\n")
    blocking_stand(command_client, timeout_sec=10)


if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)