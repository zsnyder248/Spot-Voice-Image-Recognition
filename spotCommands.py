import Estop
from Spot import Spot
import sys
import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util
import bosdyn.geometry
import time

from bosdyn.client.image import ImageClient
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient, blocking_stand

isMoving = False
moveForward = False
moveBackward = False
moveLeft = False
MoveRight = False
SPEED = 1.0

def main(argv):
    # username = str(sys.argv[2])
    # password = str(sys.argv[4])
    # hostname = str(sys.argv[5])
    print("HI")
    username = 'user'
    password = 'dy8dtr33sv6p'
    hostname = '192.168.80.3'
    robot = Spot(username, password, hostname)
    robot.auth()

    if(robot == False):
        print("Error while initializing Spot. Exiting...")
        sys.exit()
    togglePower(robot)
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
    if "forward" in command: # Spot forward
        if "step forward" in command: # Spot step forward
            spotStepForward(robot, 1)
        elif "meters" in command: # Spot forward 2 meters || spot move forward 2 meters
            spotForwardDistance(robot, (command.split("meters")[0]).split(" ")[-2])
        elif "toggle" in command:
            spotToggleForward(robot)
    elif "backward" in command: # Spot backward
        if "step backward" in command: # Spot step backward/backwards
            spotStepBackward(robot, 1)
        elif "meters" in command: # Spot backward 2 meters || spot move backward 2 meters
            spotBackwardDistance(robot, (command.split("meters")[0]).split(" ")[-2])
        elif "toggle" in command:
            spotToggleBackward(robot)
    elif "turn" in command:
        if "turn right" in command:
            spotTurnRight(robot)
        elif "turn left" in command:
            spotTurnLeft(robot) 
    elif "right" in command: # Spot right
        if "step right" in command: # Spot step right
            spotStepRight(robot, 1)
        elif "meters" in command: # Spot right 2 meters || spot move right 2 meters
            spotRightDistance(robot, (command.split("meters")[0]).split(" ")[-2])
        elif "toggle" in command:
            spotToggleRight(robot)
    elif "left" in command: # Spot left
        if "step left" in command: # Spot step left
            spotStepLeft(robot, 1)
        elif "meters" in command: # Spot left 2 meters || spot move left 2 meters
            spotLeftDistance(robot, (command.split("meters")[0]).split(" ")[-2])
        elif "toggle" in command:
            spotToggleLeft(robot) 
    elif "sit" in command:
        spotSit(robot)
    elif "stand" in command:
        spotStand(robot)

# Forward Movements #
def spotForwardDistance(robot, distance):
    moveForward = True
    try:
        print("Spot is walking forward\n")
        robot.forward(distance/SPEED, SPEED)
    except KeyboardInterrupt:
        moveForward = False  

def spotToggleForward(robot):
    moveForward = True
    while(moveForward):
        try:
            print("Spot is walking forward\n")
            robot.forward(0.5, SPEED)
            time.sleep(0.5) # this might need to be different
        except KeyboardInterrupt:
            moveForward = False
            break  

def spotStepForward(robot, numSteps):
    print("Spot stepping forward\n")
    robot.forward(1, numSteps, SPEED)

# End Forward Movements #

# Backward Movements #
def spotBackwardDistance(robot, distance):
    moveBackward = True
    try:
        print("Spot is walking Backward\n")
        robot.backward(distance/SPEED, SPEED)
    except KeyboardInterrupt:
        moveBackward = False  

def spotToggleBackward(robot):
    moveBackward = True
    while(moveBackward):
        try:
            print("Spot is walking Backward\n")
            robot.backward(0.5, SPEED)
            time.sleep(0.5) # this might need to be different
        except KeyboardInterrupt:
            moveBackward = False
            break  

def spotStepBackward(robot, numSteps):
    print("Spot stepping Backward\n")
    robot.backward(1, numSteps, SPEED)

# End Backward Movements #

# Right Movements #
def spotRightDistance(robot, distance):
    moveRight = True
    try:
        print("Spot is walking Right\n")
        robot.moveRight(distance/SPEED, SPEED)
    except KeyboardInterrupt:
        moveRight = False  

def spotToggleRight(robot):
    moveRight = True
    while(moveRight):
        try:
            print("Spot is walking Right\n")
            robot.moveRight(0.5, SPEED)
            time.sleep(0.5) # this might need to be different
        except KeyboardInterrupt:
            moveRight = False
            break  

def spotStepRight(robot, numSteps):
    print("Spot stepping Right\n")
    robot.moveRight(1, numSteps, SPEED)

def spotTurnRight(robot):
    print("Spot turning right\n")
    robot.turnRight()

# End Right Movements #

# Left Movements #
def spotLeftDistance(robot, distance):
    moveLeft = True
    try:
        print("Spot is walking Left\n")
        robot.moveLeft(distance/SPEED, SPEED)
    except KeyboardInterrupt:
        moveLeft = False  

def spotToggleLeft(robot):
    moveLeft = True
    while(moveLeft):
        try:
            print("Spot is walking Left\n")
            robot.moveLeft(0.5, SPEED)
            time.sleep(0.5) # this might need to be different
        except KeyboardInterrupt:
            moveLeft = False
            break  

def spotStepLeft(robot, numSteps):
    print("Spot stepping Left\n")
    robot.moveLeft(1, numSteps, SPEED)

def spotTurnLeft(robot):
    print("Spot turning Left\n")
    robot.turnLeft()

# End Left Movements #

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