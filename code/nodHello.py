from picarx import Picarx
from vilib import Vilib
import time

def detect_face():
    # Check for faces
    num_faces = Vilib.detect_obj_parameter['human_n']
    return num_faces > 0

if __name__ == "__main__":
    try:
        # Initialize camera for face detection
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.face_detect_switch(True)
        Vilib.display(local=True, web=False)
        time.sleep(2)
        
        px = Picarx()
        original_speed = 10
        stopped_speed = 0
        
        px.forward(original_speed)
        time.sleep(0.5)

        while True:
            # Check for face detection
            if detect_face():
                # Stop the car when a face is detected
                px.forward(stopped_speed)
                time.sleep(1)

                # Nodding behavior
                for angle in range(0, 35):
                    px.set_camera_servo2_angle(angle)
                    time.sleep(0.01)
                for angle in range(35, -35, -1):
                    px.set_camera_servo2_angle(angle)
                    time.sleep(0.01)
                for angle in range(-35, 0):
                    px.set_camera_servo2_angle(angle)
                    time.sleep(0.01)
                
                # Turn direction to the right and move forward
                px.set_dir_servo_angle(30)
                px.forward(original_speed)
                time.sleep(1)
                
                # Stop completely and end the program
                px.forward(0)
                break

    finally:
        # Close the camera stream
        Vilib.camera_close()
        px.forward(0)
