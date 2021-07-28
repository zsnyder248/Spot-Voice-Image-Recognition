"""
Project: AI Robot - Human Following
Author: Jitesh Saini
Github: https://github.com/jiteshsaini
website: https://helloworld.co.in

The code in this file is same as 'human_follower.py' file. However, code with respect to FLASK implementation has been removed.
So there is no streaming of camera view. This is bare minimum human following robot.
"""
# System modules
import sys
import time
from threading import Thread

# Misc. modules
import cv2
import numpy as np
from PIL import Image

# Custom modules
import common as cm

# Class for providing object tracking and translation to Spot movements
class ObjectTracker:

    def __init__(self, obj, spotAPI):

        # Initialize model information
        self.model_dir = '/all_models'
        self.model_edgetpu = 'mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite'
        self.lbl = 'coco_labels.txt'

        # Initialize CV
        self.cap = cv2.VideoCapture(0)
        self.threshold = 0.2
        self.top_k = 5 # Number of objects to be shown as detected
        self.edgetpu = 1
        self.tolerance = 0.1
        self.x_deviation = 0
        self.y_max = 0

        # Define object to be tracked
        self.object_to_track = obj

        # Store Spot API for controls
        self.spotAPI = spotAPI

        # Call main function and start async tracking
        self.__isTracking = True
        thread = Thread(target = self.main)
        thread.start()

    """ def toggleTracking(self):
        self.__isTracking = not(self.__isTracking)
    """
    
    def endTracking(self):
        self.__isTracking = False

    def track_object(self, objs, labels):
        
        if (len(objs) == 0):
            print("No objects to track.")
            return

        flag = 0
        for obj in objs:
            lbl = labels.get(obj.id, obj.id)
            if (lbl == self.object_to_track):
                x_min, y_min, x_max, self.y_max = list(obj.bbox)
                flag=1
                break
            
        #print(x_min, y_min, x_max, y_max)
        if(flag==0):
            print("Selected object not present.")
            return
            
        x_diff=x_max-x_min
        y_diff=self.y_max-y_min
            
        obj_x_center=x_min+(x_diff/2)
        obj_x_center=round(obj_x_center,3)
        
        obj_y_center=y_min+(y_diff/2)
        obj_y_center=round(obj_y_center,3)
        
        self.x_deviation=round(0.5-obj_x_center,3)
        self.y_max=round(self.y_max,3)
            
        print("{",self.x_deviation,self.y_max,"}")
    
        thread = Thread(target = self.move_robot)
        thread.start()
        

    def move_robot(self):
        
        y = 1 - self.y_max # Distance from bottom of the frame
        
        if (abs(self.x_deviation) < self.tolerance):
            
            # Put Spot into a standing position
            if (y<0.1):
                self.spotAPI.genericMovement("stand")
                print("reached object...........")

            # Move Spot forward        
            else:
                self.spotAPI.genericMovement("W")
                print("moving robot ...FORWARD....!!!!!!!!!!!!!!")
 
        else:

            # Turn Spot to the left
            if (self.x_deviation >= self.tolerance):
                delay1 = self.get_delay(self.x_deviation)   
                self.spotAPI.genericMovement("E")
                time.sleep(delay1)
                print("moving robot ...Left....<<<<<<<<<<")
            
            # Turn Spot to the right
            if (self.x_deviation <= -1 * self.tolerance):
                delay1 = self.get_delay(self.x_deviation)
                self.spotAPI.genericMovement("Q")
                time.sleep(delay1)
                print("moving robot ...Right....>>>>>>>>")
        
    def get_delay(self, deviation):
        
        deviation=abs(deviation)
        
        if(deviation>=0.4):
            d=0.080
        elif(deviation>=0.35 and deviation<0.40):
            d=0.060
        elif(deviation>=0.20 and deviation<0.35):
            d=0.050
        else:
            d=0.040
        
        return d

    def main(self):
    
        interpreter, labels = cm.load_model(self.model_dir,self.model_edgetpu,self.lbl,self.edgetpu)
        
        fps=1
    
        while self.__isTracking == True:
            start_time=time.time()
            
            #----------------self.capture Camera Frame-----------------
            ret, frame = self.cap.read()
            if not ret:
                break
            
            cv2_im = frame
            cv2_im = cv2.flip(cv2_im, 0)
            cv2_im = cv2.flip(cv2_im, 1)

            cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(cv2_im_rgb)
        
            #-------------------Inference---------------------------------
            cm.set_input(interpreter, pil_im)
            interpreter.invoke()
            objs = cm.get_output(interpreter, score_threshold=self.threshold, top_k=self.top_k)
            
            #-----------------other------------------------------------
            self.track_object(objs,labels)#tracking  <<<<<<<
        
            fps = round(1.0 / (time.time() - start_time),1)
            print("*********FPS: ",fps,"************")

        self.cap.release()
        cv2.destroyAllWindows()

