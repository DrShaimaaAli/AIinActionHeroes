# this code enables car to stop when it detects an object, then determines a clear path and continues. 
# when the car stops, it turns the red light on and then when the path is clear it has the green light on.

# Importing necessary modules for LED, motor, servo, GPIO and time operations
from Led import *
from Motor import *
from servo import *
import RPi.GPIO as GPIO
import time

# Class definition for advanced ultrasonic functionality with LED feedback
class AdvancedUltrasonicWithLED:
    def __init__(self):
        # Disabling warnings
        GPIO.setwarnings(False)
        
        # Setting up GPIO pins for the ultrasonic sensor
        self.trigger_pin = 27
        self.echo_pin = 22
        
        # Setting maximum distance for the ultrasonic sensor and timeout
        self.MAX_DISTANCE = 300
        self.timeOut = self.MAX_DISTANCE * 60
        
        # Setting GPIO mode and initializing pins for trigger and echo
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
        # Initializing motor, servo and LED
        self.PWM = Motor()
        self.pwm_S = Servo()
        self.led = Led()

    # Method to get the pulse duration
    def pulseIn(self, pin, level, timeOut):
        t0 = time.time()
        
        # Wait until pin reads as high level
        while(GPIO.input(pin) != level):
            if((time.time() - t0) > timeOut * 0.000001):
                return 0
        
        # Reset timer
        t0 = time.time()
        
        # Wait until pin reads as low level
        while(GPIO.input(pin) == level):
            if((time.time() - t0) > timeOut * 0.000001):
                return 0
        
        # Calculate pulse duration
        pulseTime = (time.time() - t0) * 1000000
        return pulseTime

    # Method to get distance using the ultrasonic sensor
    def get_distance(self):
        # List to store distance readings
        distance_cm = [0, 0, 0, 0, 0]
        
        # Take 5 distance readings
        for i in range(5):
            GPIO.output(self.trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.trigger_pin, GPIO.LOW)
            
            # Get pulse duration
            pingTime = self.pulseIn(self.echo_pin, GPIO.HIGH, self.timeOut)
            
            # Calculate distance
            distance_cm[i] = pingTime * 340.0 / 2.0 / 10000.0
        
        # Sort distances and return the median value
        distance_cm = sorted(distance_cm)
        return int(distance_cm[2])



## main functions for the obstacle avoidance program

    # Method to control the motor based on distance readings
    # this function stops the car if it detects obstacle within 30 cm then calls the avoidance function
    def control_motor(self):
        
        while True:
            # Get distance from the front
            M = self.get_distance()
            
            # If distance is more than 30cm, move forward and turn on green LED
            if M > 30:
                self.PWM.setMotorModel(1000, 1000, 1000, 1000)
                # Green LED
                self.led.ledIndex(0x01, 0, 255, 0)  
                self.led.ledIndex(0x02, 0, 255, 0)  
                self.led.ledIndex(0x04, 0, 255, 0)  
                self.led.ledIndex(0x08, 0, 255, 0)  
                self.led.ledIndex(0x10, 0, 255, 0)  
                self.led.ledIndex(0x20, 0, 255, 0)  
                self.led.ledIndex(0x40, 0, 255, 0)  
                self.led.ledIndex(0x80, 0, 255, 0)  
                

            # If distance is less than 30cm, stop, turn on red LED, and try to avoid the obstacle
            else:
                self.PWM.setMotorModel(0, 0, 0, 0)
                 # Red LED
                self.led.ledIndex(0x01, 255, 0, 0)  
                self.led.ledIndex(0x02, 255, 0, 0)  
                self.led.ledIndex(0x04, 255, 0, 0)  
                self.led.ledIndex(0x08, 255, 0, 0)  
                self.led.ledIndex(0x10, 255, 0, 0)  
                self.led.ledIndex(0x20, 255, 0, 0)  
                self.led.ledIndex(0x40, 255, 0, 0)  
                self.led.ledIndex(0x80, 255, 0, 0) 
                
                self.avoid_obstacle()

    # Method to avoid obstacles
    def avoid_obstacle(self):
        # Dictionary to store distances in different directions
        distances = {}
        
        # Check distances on left, middle and right directions
        for angle in [30, 90, 150]:
            self.pwm_S.setServoPwm('0', angle) # rotate the servo to the specified angle
            time.sleep(0.2) # Wait for the servo to move to the position
            distances[angle] = self.get_distance() # for each angle, get the distance from the sensor
        
        # Determine the angle with the max clearance distance
        max_distance_angle = max(distances, key=distances.get)
        
        # Move backward for 0.1 seconds
        self.PWM.setMotorModel(-800, -800, -800, -800)
        time.sleep(0.1)
        
        # Turn in the direction of most clearance
        if max_distance_angle == 30:  # Turn left
            self.PWM.setMotorModel(-2000, -2000, 2000, 2000)
        elif max_distance_angle == 150:  # Turn right
            self.PWM.setMotorModel(2000, 2000, -2000, -2000)
        
        # Allow some time for the car to turn
        time.sleep(0.5)

        #re-set servo angle to middle 90d
        self.pwm_S.setServoPwm('0', 90)


    # Main method to start the motor control
    def run(self):
        self.control_motor()

# Main program execution
if __name__ == '__main__':
    print('Program is starting ... ')
    ultrasonic = AdvancedUltrasonicWithLED()
    
    # Try running the ultrasonic functionality and handle any interruptions
    try:
        ultrasonic.run()
    except KeyboardInterrupt:  # Stop on keyboard interrupt (Ctrl+C)
        ultrasonic.PWM.setMotorModel(0, 0, 0, 0)  # Stop the motor
        ultrasonic.pwm_S.setServoPwm('0', 90)  # Reset the servo position
        ultrasonic.led.colorWipe(ultrasonic.led.strip, Color(0, 0, 0))  # Turn off the LED
