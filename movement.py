from gpiozero import Motor, Servo
from time import sleep

# Motor pins (adjust GPIO numbers as needed)
motor_left = Motor(forward=17, backward=18)
motor_right = Motor(forward=22, backward=23)

# Servo pins (steering)
servo_left = Servo(5)
servo_right = Servo(6)

def set_steering(direction):
    if direction == "straight":
        servo_left.value = 0
        servo_right.value = 0
    elif direction == "left":
        servo_left.value = 0.7
        servo_right.value = -0.7
    elif direction == "right":
        servo_left.value = -0.7
        servo_right.value = 0.7

def go_forward():
    set_steering("straight")
    motor_left.forward()
    motor_right.forward()

def go_backward():
    set_steering("straight")
    motor_left.backward()
    motor_right.backward()

def turn_left():
    set_steering("left")
    motor_left.forward()
    motor_right.forward()

def turn_right():
    set_steering("right")
    motor_left.forward()
    motor_right.forward()

def stop():
    motor_left.stop()
    motor_right.stop()
    set_steering("straight")

# Test sequence
try:
    print("Moving forward")
    go_forward()
    sleep(2)

    print("Turning right")
    turn_right()
    sleep(1)

    print("Turning left")
    turn_left()
    sleep(1)

    print("Going backward")
    go_backward()
    sleep(2)

    print("Stopping")
    stop()

except KeyboardInterrupt:
    stop()
    print("Program stopped")
