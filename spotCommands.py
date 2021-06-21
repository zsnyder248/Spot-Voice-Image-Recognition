import Estop
from Spot import Spot
import sys
import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util
import bosdyn.geometry

from bosdyn.client.image import ImageClient
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient, blocking_stand

isMoving = False

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
    isMoving = False
    command = command.replace("spot ", "")
    print("Command: " + command + "\n")
    isMoving = True
    if "forward" in command:
        if "step forward" in command:
            spotForward(robot, 1)
        else:
            spotForward(robot, 0)
    elif "backward" in command:
        spotBackward(robot)
    elif "right" in command:
        if "turn right" in command:
            spotTurnRight(robot)
        else:
            spotMoveRight(robot)
    elif "left" in command:
        if "turn left" in command:
            spotTurnLeft(robot)
        else:
            spotMoveLeft(robot)
    elif "sit" in command:
        spotSit(robot)
    elif "stand" in command:
        spotStand(robot)

def spotForward(robot, num):
    if(num == 1):
        print("Spot stepping forward\n")
        robot.forward()
    else:
        while(True):
            robot.forward()
            if(isMoving == False):
                break

def spotBackward(robot):
    print("Spot moving backward\n")
    robot.backward()

def spotMoveRight(robot):
    print("Spot moving to the right\n")
    robot.moveRight()

def spotTurnRight(robot):
    print("Spot turning right\n")
    robot.turnRight()

def spotMoveLeft(robot):
    print("Spot moving to the left\n")
    robot.moveLeft()

def spotTurnLeft(robot):
    print("Spot turning left\n")
    robot.turnLeft()

def spotSit(robot):
    print("Spot sitting\n")
    robot.sit()

def spotStand(robot):
    print("Spot standing\n")
    robot.stand()


if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)
# main()