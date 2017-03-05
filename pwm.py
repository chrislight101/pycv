import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.OUT) #in1
GPIO.setup(12, GPIO.OUT) #in2
GPIO.setup(13, GPIO.OUT) #in3

p = GPIO.PWM(13,50)

GPIO.output(11, 1)
GPIO.output(12, 0)

p.start(100)

time.sleep(3)

p.stop()

GPIO.cleanup()


