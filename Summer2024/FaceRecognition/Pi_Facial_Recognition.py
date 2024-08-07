import cv2
from picamera2 import Picamera2

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

while True:
    im = picam2.capture_array()
    im, face_count = detect_face(im)  # Receive both the image and the face count
    print("Faces detected:", face_count)  
    cv2.imshow("Face", im)
    if cv2.waitKey(1) == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
