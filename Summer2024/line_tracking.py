import time
from Motor import *
import RPi.GPIO as GPIO


class Line_Tracking:
    def __init__(self):
        self.IR01 = 14 # left sensor
        self.IR02 = 15 # middle sensor
        self.IR03 = 23 # right sensor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01, GPIO.IN)
        GPIO.setup(self.IR02, GPIO.IN)
        GPIO.setup(self.IR03, GPIO.IN)

        # Initializing motor
        self.PWM = Motor()

    def run(self):
        while True:
            self.LMR = 0x00
            if GPIO.input(self.IR01):  # left sensor detect line since 4 is 100 in binary
                self.LMR |= 4
            if GPIO.input(self.IR02):  # middle sensor detect line since 2 is 010 in binary
                self.LMR |= 2
            if GPIO.input(self.IR03):  # right sensor detect line since 1 is 001 in binary
                self.LMR |= 1

            # Line tracking logic
            if self.LMR == 2:  # moves forward since middle sensor detect line
                self.PWM.setMotorModel(800, 800, 800, 800)
            elif self.LMR == 4:  # moves left slightly since left sensor detect line
                self.PWM.setMotorModel(-1500, -1500, 2500, 2500)
            elif self.LMR == 6:  # moves left since left and middle sensor detect line
                self.PWM.setMotorModel(-2000, -2000, 4000, 4000)
            elif self.LMR == 1:  # moves right slightly since right sensor detect line
                self.PWM.setMotorModel(2500, 2500, -1500, -1500)
            elif self.LMR == 3:  # moves right since right and middle sensor detect line
                self.PWM.setMotorModel(4000, 4000, -2000, -2000)
            elif self.LMR == 7:  # stop since all sensors detect line
                self.PWM.setMotorModel(0, 0, 0, 0)
            else:  # if no line is detected by any sensor, stop
                self.PWM.setMotorModel(0, 0, 0, 0)


# Main program logic follows:
if __name__ == '__main__':
    print('Program is starting ... ')
    infrared = Line_Tracking()

    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program will be executed.
        infrared.PWM.setMotorModel(0, 0, 0, 0)
