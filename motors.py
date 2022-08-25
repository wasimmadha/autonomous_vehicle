#!/usr/bin/env python3
import RPi.GPIO as GPIO
from datetime import datetime
import time
import pandas as pd
import pygame  #Used pygame to detect keypresses
from tflite_runtime.interpreter import Interpreter
import cv2
import numpy as np


def predict(img,model_path):
    tflite_interpreter = Interpreter(model_path=model_path)

    input_details = tflite_interpreter.get_input_details()
    output_details = tflite_interpreter.get_output_details()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, dsize=(96, 96), interpolation=cv2.INTER_CUBIC)
    img = img.reshape(96, 96, 1)

    img = np.float32(img)
    input_tensor= np.array(np.expand_dims(img,0), dtype=np.float32)
    tflite_interpreter.allocate_tensors()
    tflite_interpreter.set_tensor(input_details[0]['index'],input_tensor)
    tflite_interpreter.invoke()
    output_details = tflite_interpreter.get_output_details()
    
    pred = tflite_interpreter.get_tensor(output_details[0]['index'])
    result = np.argmax(pred)
    return result


# Speed Parameters
FORWARD_SPEED = 40
SIDE_SPEED = 85

# Initialise Pygame
pygame.init()

# Data to be stored in CSV
timeStamps = []
IR1 = []
IR2 = []
action = []

#used for print statement to debug
debug = False

#to use with sensor driven:manual or ai driven:auto
modes = ["manual","auto"]
mode = modes[1]

def setup():
    # Set PWM Pin with frequency of 1khz
    frequency = 5000
    
    GPIO.setmode(GPIO.BCM)
    
    # For Right Motor
    Right_CW = 13
    Right_CCW = 6
    ENRight = 20
    
    # For Left Motor
    Left_CW = 26
    Left_CCW = 19
    ENLeft = 21
    
    # IR Sensors
    sensor_1 = 4
    sensor_2 = 17

    
    # Pin Setup
    # Setup for right motors
    GPIO.setup(Right_CW,GPIO.OUT)
    GPIO.setup(Right_CCW,GPIO.OUT)
    GPIO.setup(ENRight,GPIO.OUT)
    
    # Setup for left motors
    GPIO.setup(Left_CW,GPIO.OUT)
    GPIO.setup(Left_CCW,GPIO.OUT)
    GPIO.setup(ENLeft,GPIO.OUT)
    
    # Setup for Sensors
    GPIO.setup(sensor_1,GPIO.IN)
    GPIO.setup(sensor_2,GPIO.IN)
    
    # PWM Configurations 
    Right_PWM = GPIO.PWM(ENRight,frequency)
    Left_PWM = GPIO.PWM(ENLeft,frequency)
    
    # Intialise with 0
    # One time initialisation for PWM, .start(), used to set an intial PWM value
    Right_PWM.start(0)
    Left_PWM.start(0)
    
    GPIO.setwarnings(False)
        
    return Right_PWM, Right_CW, Right_CCW, Left_PWM, Left_CCW, Left_CW, sensor_1, sensor_2


def movement(move_direction, Right_PWM, Left_PWM, Right_CW, Left_CW,Right_CCW,Left_CCW,R_PWM_value = 0,L_PWM_value=0):
        
    #store action
    action.append(move_direction)
    
    # Used technique: All GPIO pins false, conditionally we will make GPIO pins True according to our convenience 
    GPIO.output(Left_CW,False)
    GPIO.output(Right_CW,False)
    GPIO.output(Left_CCW,False)
    GPIO.output(Right_CCW,False)
    
    if(move_direction == "STOP"):
            Right_PWM.ChangeDutyCycle(R_PWM_value)
            Left_PWM.ChangeDutyCycle(L_PWM_value)
            
    elif(move_direction == "RIGHT"):
        
            # Set Right PWM to 0 and Left PWM to 30
            # Enable left motors on
            Right_PWM.ChangeDutyCycle(R_PWM_value)
            Left_PWM.ChangeDutyCycle(L_PWM_value)
            GPIO.output(Right_CW,True)
            GPIO.output(Left_CCW,True)      
            
            
    elif(move_direction == "LEFT"):
            # Set Right PWM to 0 and Left PWM to 30
            # Enable left motors on
            Right_PWM.ChangeDutyCycle(R_PWM_value)
            Left_PWM.ChangeDutyCycle(L_PWM_value)
            
            GPIO.output(Left_CW,True)
            GPIO.output(Right_CCW,True)
            
    elif(move_direction == "FORWARD"):
            Left_PWM.ChangeDutyCycle(L_PWM_value)
            Right_PWM.ChangeDutyCycle(R_PWM_value)
            GPIO.output(Left_CW,True)
            GPIO.output(Right_CW,True)
        
        
    # match move_direction:
    #     case "STOP":
    #         # Set Both PWMs to 0 to stop
    #         Right_PWM.ChangeDutyCycle(R_PWM_value)
    #         Left_PWM.ChangeDutyCycle(L_PWM_value)

    #     case "RIGHT":
    #         # Set Right PWM to 0 and Left PWM to 30
    #         # Enable left motors on
    #         Right_PWM.ChangeDutyCycle(R_PWM_value)
    #         Left_PWM.ChangeDutyCycle(L_PWM_value)
    #         GPIO.output(Left_CW,True)
        
    #     case "LEFT":
    #         # Set Left PWM to 0 and Right PWM to 30
    #         # Enable right motors on
    #         Right_PWM.ChangeDutyCycle(R_PWM_value)
    #         Left_PWM.ChangeDutyCycle(L_PWM_value)
    #         GPIO.output(Right_CW,True)

    #     case "FORWARD":
    #         # Set Both PWMs to 30 for forward
    #         Left_PWM.ChangeDutyCycle(L_PWM_value)
    #         Right_PWM.ChangeDutyCycle(R_PWM_value)
    #         GPIO.output(Left_CW,True)
    #         GPIO.output(Right_CW,True)
       
        
        
        
    

flag = False

if __name__ == "__main__":
    
    delay_in_turn = 0.05  #Delay produced for coarse correction of track
    
    Right_PWM, Right_CW, Right_CCW, Left_PWM, Left_CCW, Left_CW, sensor_1, sensor_2 = setup()
    
    try:
        while True:
            time.sleep(0.05) #Delay produced to eliminate random zero values of sensors
            
            # datetime object containing current date and tzime
            now = datetime.now()

            # Date Time String
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            vid = cv2.VideoCapture(0)

            #read and print sensor data in manual mode
            if mode == "manual":
                sensor_1_data = GPIO.input(sensor_1)
                sensor_2_data = GPIO.input(sensor_2)
                
                print(f"Sensor 1 Data : {sensor_1_data}") if debug else None
                print(f"Sensor 2 Data : {sensor_2_data}") if debug else None
                
                #store timestamp
                timeStamps.append(dt_string)
                
                # Store sensor data
                IR1.append(sensor_1_data)
                IR2.append(sensor_2_data)
                

            #for now vehicle can be in two modes i.e auto or manual   
            if(mode == "manual"):
                if(sensor_1_data == 0 and sensor_2_data == 0):
                        movement("STOP",Right_PWM,Left_PWM,Right_CW,Left_CW,Right_CCW,Left_CCW,R_PWM_value = 0,L_PWM_value=0)
                elif(sensor_1_data == 1 and sensor_2_data == 0):
                        movement("RIGHT",Right_PWM,Left_PWM,Right_CW,Left_CW,Right_CCW,Left_CCW,R_PWM_value = SIDE_SPEED,L_PWM_value=SIDE_SPEED)
                        time.sleep(delay_in_turn*2)
                elif(sensor_1_data == 0 and sensor_2_data == 1):
                        movement("LEFT",Right_PWM,Left_PWM,Right_CW,Left_CW,Right_CCW,Left_CCW,R_PWM_value = SIDE_SPEED,L_PWM_value=SIDE_SPEED)
                        time.sleep(delay_in_turn*2)
                else:
                        movement("FORWARD",Right_PWM,Left_PWM,Right_CW,Left_CW,Right_CCW,Left_CCW,R_PWM_value = FORWARD_SPEED,L_PWM_value=FORWARD_SPEED)
            elif(mode == "auto"):
                ret, frame = vid.read()
                result = predict(frame, model_path="models\model_1\model1.tflite")

                if result == 0:
                        print(result)
                        # movement("FORWARD",Right_PWM,Left_PWM,Right_CW,Left_CW,Right_CCW,Left_CCW,R_PWM_value = FORWARD_SPEED,L_PWM_value=FORWARD_SPEED)
                elif result == 1:
                        print(result)
                        # movement("RIGHT",Right_PWM,Left_PWM,Right_CW,Left_CW,Right_CCW,Left_CCW,R_PWM_value = SIDE_SPEED,L_PWM_value=SIDE_SPEED)
                        # time.sleep(delay_in_turn*2)
                elif result == 2:
                        print(result)
                        # movement("LEFT",Right_PWM,Left_PWM,Right_CW,Left_CW,Right_CCW,Left_CCW,R_PWM_value = SIDE_SPEED,L_PWM_value=SIDE_SPEED)
                        # time.sleep(delay_in_turn*2)
                else:
                        print(result)


                
            # match mode:
            #     #in manual mode : forward left right stop condition can exit , later backward can be implemented
            #     case "manual":
            #         if(sensor_1_data == 0 and sensor_2_data == 0):
            #             movement("STOP",Right_PWM,Left_PWM,Right_CW,Left_CW,R_PWM_value = 0,L_PWM_value=0)
            #         elif(sensor_1_data == 1 and sensor_2_data == 0):
            #             movement("RIGHT",Right_PWM,Left_PWM,Right_CW,Left_CW,R_PWM_value = 0,L_PWM_value=30)
            #         elif(sensor_1_data == 0 and sensor_2_data == 1):
            #             movement("LEFT",Right_PWM,Left_PWM,Right_CW,Left_CW,R_PWM_value = 30,L_PWM_value=0)
            #         else:
            #             movement("FORWARD",Right_PWM,Left_PWM,Right_CW,Left_CW,R_PWM_value = 30,L_PWM_value=30)
                
            #     case "auto":
            #         pass

            # On keyboard press, safely exit the program
        #     for event in pygame.event.get():
        #         if event.type == pygame.KEYDOWN:
        #             print("Keydown Pressed") if debug else None
                    
        #             #File saving
        #             dict_data  = {'timeStamp' : timeStamps, 'IR1' : IR1, 'IR2' : IR2, 'ACTION' : action}
        #             df = pd.DataFrame(dict_data)
                    
        #             #Saving the dataframe
        #             df.to_csv('DataSamples/data_ir.csv',index=False)
        #             flag = True
                
        #             break
            
        #     if flag:
        #         break

                
    except Exception as e:
        print(e)
        
    finally:
        print("Program exits successfully") 
        GPIO.cleanup()