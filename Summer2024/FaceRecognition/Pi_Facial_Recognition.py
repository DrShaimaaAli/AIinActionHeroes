import cv2
from picamera2 import Picamera2
from servo import *
from Led import *

"""
To install necessary libraries, run the following commands in the terminal:

sudo apt update
sudo apt upgrade
sudo apt install python3-opencv

Verify installation in the terminal:

python
import cv2
print(cv2.__version__)
exit()

Download Haar Cascade file:

https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
Save Haar Cascade file in the same file as python code
When using cv2.CascadeClassifier, use the file path as the parameter
"""

servo = Servo()
led = Led()

face_cascade = cv2.CascadeClassifier('/home/pi/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server/haarcascade_frontalface_default.xml')

def detect_face(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_img, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (20, 255, 0), 4)
    return img, len(faces)  # Return the image and the count of faces

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)  # Full screen: 3280 2464
picam2.preview_configuration.main.format = "RGB888"  # 8 bits
picam2.start()

try:
    while True:
        servo.setServoPwm('0', 90)
        servo.setServoPwm('1', 130)
        im = picam2.capture_array()
        im, face_count = detect_face(im)  # Receive both the image and the face count
        print("Faces detected:", face_count) 

        if face_count > 0:
            led.ledIndex(0x01, 0, 255, 0)
            led.ledIndex(0x02, 0, 255, 0) 
            led.ledIndex(0x04, 0, 255, 0) 
            led.ledIndex(0x08, 0, 255, 0) 
            led.ledIndex(0x10, 0, 255, 0) 
            led.ledIndex(0x20, 0, 255, 0)    
            led.ledIndex(0x40, 0, 255, 0) 
            led.ledIndex(0x80, 0, 255, 0)  # green lights 
        else:
            led.ledIndex(0x01, 255, 0, 0)
            led.ledIndex(0x02, 255, 0, 0)
            led.ledIndex(0x04, 255, 0, 0) 
            led.ledIndex(0x08, 255, 0, 0) 
            led.ledIndex(0x10, 255, 0, 0) 
            led.ledIndex(0x20, 255, 0, 0)  
            led.ledIndex(0x40, 255, 0, 0) 
            led.ledIndex(0x80, 255, 0, 0)  # red lights

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    led.colorWipe(led.strip, Color(0,0,0))          #turn off the light
    picam2.stop()
    print("Camera stopped.")
