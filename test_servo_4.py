import RPi.GPIO as GPIO
import time

P_SERVO1 = 17
P_SERVO2 = 27 # GPIO端口号，根据实际修改
fPWM = 50  # Hz (软件PWM方式，频率不能设置过高)
a = 10
b = 2

def setup():
    global pwm
    global pwm2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(P_SERVO1, GPIO.OUT)
    pwm = GPIO.PWM(P_SERVO1, fPWM)
    pwm.start(0)
    GPIO.setup(P_SERVO2, GPIO.OUT)
    pwm2 = GPIO.PWM(P_SERVO2, fPWM)
    pwm2.start(0)

def setDirection(direction):
    duty = direction#a / 180 * direction 
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.8) 

def setDirection2(direction):
    duty = direction
    pwm2.ChangeDutyCycle(duty)
    time.sleep(1.5) 
   
setup()
# for direction in range(120, 0, -10):
#     setDirection(direction)

direction = 0    
setDirection(25)    
# time.sleep(1)
setDirection(0)    
setDirection2(23)    

setDirection2(0)    
GPIO.cleanup() 
