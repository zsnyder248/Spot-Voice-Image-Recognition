import Estop
from Spot import Spot
import sys
import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util
import bosdyn.geometry

from bosdyn.client.image import ImageClient
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient, blocking_stand

def main(argv):
    # username = str(sys.argv[2])
    # password = str(sys.argv[4])
    # hostname = str(sys.argv[5])
    print("HI")
    username = 'user'
    password = 'h6mvzmpghunc'
    hostname = '192.168.80.3'
    robot = Spot(username, password, hostname)
    robot.auth()

    if(robot == False):
        print("Error while initializing Spot. Exiting...")
        sys.exit()

    print("Spot command.\n")

    while(True):
        command = (str(input("Enter a command (commands must start with spot) or enter 'end' to stop commanding spot: "))).lower()
        print("\n")

        # command = command.lower()

        if(command == "stop" or command == "estop"):
            spotEstop(robot)
            break
        elif(command == "end"):
            spotShutdown(robot)
            break
        elif(command == "power"):
            togglePower(robot)
        elif "spot" not in command:
            print("Command does not begin with spot. Spot doesn't know you're talking to him.\n")
        else:
            selectCommand(command, robot)


def togglePower(robot):
    robot.togglePower()

def spotEstop(robot):
    print("Spot EMERGENCY stop\n")
    robot.eStop()

def spotShutdown(robot):
    print("Spot shutdown\n")
    robot.endConnection()

def selectCommand(command, robot):
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
    robot.genericMovement('W')

def spotBackward(robot):
    print("Spot moving backward\n")
    robot.genericMovement('S')


def spotRight(robot):
    print("Spot turning right\n")
    robot.genericMovement('D')


def spotLeft(robot):
    print("Spot turning left\n")
    robot.genericMovement('A')


def spotSit(robot):
    print("Spot sitting\n")
    robot.genericMovement('sit')


def spotStand(robot):
    print("Spot standing\n")
    robot.genericMovement('stand')


if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)
# main()