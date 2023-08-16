from picarx import Picarx
from vilib import Vilib
import time
px = Picarx()

stopToggle = False # variable that switches between True and False to determien if that car should be stopped or not
SERVO_MAX = 15.0 # defining the max angle the wheels can turn
colors = ["green", "red"]
colorToggle = -1 # variable that switches between -1 and 1 to determine which color we are currently tracking


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


def obstacleDetection(distance, threshold):
    """
    takes in the distance from the ultrasonic sensor and a threshold value of how close we will allow the car to get before braking
    """
    if distance < threshold:
        return False
    else:
        return True

def stopLight():
    global stopToggle 
    colors = Vilib.detect_obj_parameter['color_n']
    width = Vilib.detect_obj_parameter['color_w']
    height = Vilib.detect_obj_parameter['color_h']
    #print("color",width,height)
    if (colors >= 1 and (width >= 70 or height >= 70)):
        print("Test")
        stopToggle = not stopToggle
        changeColor()

def conductor(variables):
    """
    this function takes in the states from the other functions and determines if the car should stop or not
    this function exists because without it we see the functions fighting eachother causing the car to stutter when its stopping
    """
    #print(variables)
    if (variables[0] == False or variables[1] == False):
        px.stop()
        if (variables[1] == False):
            for angle in range(0, 35):
                px.set_camera_servo2_angle(angle)
                time.sleep(0.01)
            for angle in range(35, -35, -1):
                px.set_camera_servo2_angle(angle)
                time.sleep(0.01)
            for angle in range(-35, 0):
                px.set_camera_servo2_angle(angle)
                time.sleep(0.01)
    elif (stopToggle == True):
        px.stop()
    else:
        px.forward(15)


def changeColor():
    '''
    this function when called will switch the current color that the car is tracking
    '''
    global colorToggle
    colorToggle = colorToggle * -1
    color = colors[1] if colorToggle == 1 else colors[0]
    Vilib.color_detect(color)

def faceDetect():
    num_faces = Vilib.detect_obj_parameter['human_n']
    print(num_faces)
    if num_faces > 0:
        #print(num_faces)
        return False
    else:
        return True
        







def main():
    time.sleep(2) # waits 2 seconds for camera to initialize 
    # initialzes the camera 
    Vilib.camera_start(vflip=False,hflip=False)
    Vilib.display(local=True,web=False)
    Vilib.face_detect_switch(True)


    changeColor()

    
    px.forward(15) # Starts driving forward at speed 1, this function only takes integers

    # main loop
    while True:
        
        distance = px.ultrasonic.read() # collects the distance value read by the ultrasonic sensor 

        #stopLight() 
        conductor([obstacleDetection(distance,10),faceDetect()])
             
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
        px.stop()
        time.sleep(1)


        