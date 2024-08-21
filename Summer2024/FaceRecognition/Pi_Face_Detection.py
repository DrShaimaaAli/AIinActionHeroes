import cv2
from picamera2 import Picamera2
from servo import *
from Led import *

"""
Setup Instructions:

1. Install necessary libraries by running these commands in the terminal:

   sudo apt update
   sudo apt upgrade
   sudo apt install python3-opencv

2. Verify the OpenCV installation in the terminal:

   python
   import cv2
   print(cv2.__version__)
   exit()

3. Download the Haar Cascade file for facial detection:

   https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml

   Save the Haar Cascade file in the same directory as this Python code.

4. When using cv2.CascadeClassifier, provide the file path to the Haar Cascade file.
"""


# Initialize servo and LED controls
servo = Servo()
led = Led()

# Load the pre-trained Haar Cascade classifier for facial detection
face_cascade = cv2.CascadeClassifier('/home/pi/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server/haarcascade_frontalface_default.xml')

def detect_face(img):
    # Convert the image from BGR (Blue, Green, Red) to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detects faces in the grayscale image using the Haar Cascade classifier
    faces = face_cascade.detectMultiScale(gray_img, 1.1, 5, minSize=(40, 40))
    
    # Iterate over each detected face and draw a green rectangle around it
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (20, 255, 0), 4)
    
    # Return the modified image and the number of faces detected
    return len(faces), img


# Initialize the PiCamera2 module
picam2 = Picamera2()

# Configure the camera preview resolution and format
picam2.preview_configuration.main.size = (1280, 720)  # Set resolution to 1280x720 pixels
picam2.preview_configuration.main.format = "RGB888"   # Set format to RGB with 8 bits per channel
picam2.start()  # Start the camera


try:
    while True:
        # Set servo positions 
        servo.setServoPwm('0', 90)
        servo.setServoPwm('1', 120)
        
        # Capture the current frame from the camera
        im = picam2.capture_array()
        
        # Detect faces in the captured frame
        face_count, im_with_faces = detect_face(im)
        
        # Print the number of faces detected in the current frame
        print("Faces detected:", face_count) 

        # Display the video with detected faces
        cv2.imshow('Face Detection', im_with_faces)

        # Control the LED lights based on the number of faces detected
        if face_count > 0:
            # Turn all LEDs green
            led.ledIndex(0x01, 0, 255, 0)
            led.ledIndex(0x02, 0, 255, 0)
            led.ledIndex(0x04, 0, 255, 0)
            led.ledIndex(0x08, 0, 255, 0)
            led.ledIndex(0x10, 0, 255, 0)
            led.ledIndex(0x20, 0, 255, 0)
            led.ledIndex(0x40, 0, 255, 0)
            led.ledIndex(0x80, 0, 255, 0)
        else:
            # Turn all LEDs red
            led.ledIndex(0x01, 255, 0, 0)
            led.ledIndex(0x02, 255, 0, 0)
            led.ledIndex(0x04, 255, 0, 0)
            led.ledIndex(0x08, 255, 0, 0)
            led.ledIndex(0x10, 255, 0, 0)
            led.ledIndex(0x20, 255, 0, 0)
            led.ledIndex(0x40, 255, 0, 0)
            led.ledIndex(0x80, 255, 0, 0)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    # If the user presses Ctrl+C, stop the program
    print("Program stopped by user.")

finally:
    # Turn off all LEDs 
    led.colorWipe(led.strip, Color(0, 0, 0))
    
    # Stop the camera
    picam2.stop()
    print("Camera stopped.")

    # Destroy all OpenCV windows
    cv2.destroyAllWindows()

