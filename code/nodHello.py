from picarx import Picarx
from vilib import Vilib
import time
from robot_hat import TTS

px = Picarx()
tts_robot = TTS()
SERVO_MAX = 15.0 # defining the max angle the wheels can turn


def lineTracking(values, lightModifier):
    """
    this function handles keeping the car on a line
    the function takes in the values being given by the grayscale sensor and a lightModifier values which determines if the car follows a dark or light colored line
    """
    averageValue = sum(values) / len(values) # finds the average value from th 3 grayscale sensors
    # occasionally the sensor will output (0,0,0), this code stops the computer from trying to divide by 0
    averageValue = 1 if averageValue == 0 else averageValue 
    
    # this code finds the difference between the left and right sensor and points the car towards the line based on this difference
    result = (values[0] - values[2]) / averageValue 
    result = result * -1 if lightModifier else result
    return result


def detect_face_nod():
    """
    this function checks for the presence of a human face using the Vilib library. If a face is detected, it makes the camera servo perform a nodding motion.
    """
    #get number of faces from detect_obj_parameter dict which contains various object detection parameters, and 'human_n' is one of those parameters which 
    # indicates the number of human faces detected.
    num_f = Vilib.detect_obj_parameter['human_n']
    if num_f > 0:
        #speech
        #tts_robot.say("Hi how are you")        
        #nodding motion
        for angle in range(35): # gradually tilt servo angle up from 0 to 34 degrees by increasing the angle by 1 degree each time
            px.set_camera_servo2_angle(angle) #sets the tilt servo angle
            time.sleep(0.01) # delay to allow for angle adjustment and smooth motion
        for angle in range(35, -35, -1): # tilt servo back down to -34 by decreasing by 1 each time, passing through 0 degrees until -34 degrees 
            px.set_camera_servo2_angle(angle)
            time.sleep(0.01)
        for angle in range(-35, 0): #back up to -1 degree with 1 degree steps
            px.set_camera_servo2_angle(angle)
            time.sleep(0.01)


def main():
    time.sleep(2) # waits 2 seconds for camera to initialize 
    # initialzes the camera 
    Vilib.camera_start(vflip=False,hflip=False)
    Vilib.display(local=True,web=False)
    Vilib.face_detect_switch(True)
    
    px.forward(15) # Starts driving forward at speed 1, this function only takes integers

    # main loop
    while True:
        detect_face_nod()
        grayscaleData = px.get_grayscale_data() # collects a list of 3 light sensor values
        servoAngle = lineTracking(grayscaleData,False) * SERVO_MAX 
        #servoAngle = 0 # decomment and comment the line above to disable linetracking when debugging 
        px.set_dir_servo_angle(servoAngle) # sets the angle of the front wheels


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("error:%s"%e)
    finally:
        # Close the camera stream
        Vilib.camera_close()
        px.stop()
        time.sleep(1)
