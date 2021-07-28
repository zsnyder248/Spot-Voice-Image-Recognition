'''
Project: Earthrover Robot
Author: Jitesh Saini
Github: https://github.com/jiteshsaini
website: https://helloworld.co.in

'''



from Estop import Estop
from Spot import Spot
import sys
import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util
import bosdyn.geometry
import math

from bosdyn.client.image import ImageClient
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient, blocking_stand
import os, time

edgetpu=1 # If Coral USB Accelerator connected, then make it '1' otherwise '0'

m1_1 = 8
m1_2 = 11
m2_1 = 14 
m2_2 = 15 
cam_light = 17
headlight_right = 18
headlight_left = 27 
sp_light=9 

def init_gpio():
	print("HELLO")
	global robot
	username = 'user'
	password = 'dy8dtr33sv6p'
	hostname = '192.168.80.3'
	robot = Spot(username, password, hostname)
	robot.auth()
	robot.togglePower()
	spotStand(robot)

def spotStand(robot):
    print("Spot standing adnlasd \n")
    robot.stand()

def back():
    print("moving back!!!!!!")
    
def right():
	spotTurnRight(robot, 12)
	print("moving right!!!!!!")

def left():
	spotTurnLeft(robot, 12)
	print("moving left!!!!!")
	
def spotTurnLeft(robot, degrees):
    print("Spot turning Left {0} degrees\n", degrees)
    robot.turnRight(math.radians(int(degrees)), 0.25)
    time.sleep(0.35)
    
def spotTurnRight(robot, degrees):
    print("Spot turning right {0} degrees\n", degrees)
    robot.turnLeft(math.radians(int(degrees)), 0.25)
    time.sleep(0.35)
    
def forward():
	print("moving forward$$$$")
	robot.forward(1, 0.5)

def stop():
	print("Stopping!!!!")
	

def speak_tts(text,gender):
	cmd="python /var/www/html/earthrover/speaker/speaker_tts.py '" + text + "' " + gender + " &"
	os.system(cmd)
	
def camera_light(state):
	if(state=="ON"):
		print("light on")
	else:
		print("light off")
		
def head_lights(state):
	if(state=="ON"):
		print("light on")
	else:
		print("light off")
		
def red_light(state):
	if(state=="ON"):
		print("light on")
	else:
		print("light off")
	
