from picarx import Picarx
import readchar

px = Picarx()

manual = '''
Press key to choose option

    W: Forward 
    S: Backword
    F: Stop
'''

def move(operation, speed):
    if operation == 'forward':
        px.forward(speed)
    elif operation == 'stop':
        px.stop()
    else:
        print("Unkonwn operation")

def main():
    print(manual)
    status = ''
    speed = 10
    while True:
        key = readchar.readkey().lower()
        if key == 'w':
            status = 'forward'
            print("You want the car to move forward")
        elif key == 's':
            status = 'backword'
            print("You want the car to move backword")
        elif key == 'f':
            status = 'stop'
            print('You want the car to stop')
        else:
            print('Goodbye')
            break

        move(status, speed)

try:
    main()
finally:
    px.stop()
    print("Cleaning up")
