import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11,GPIO.OUT)
p=GPIO.PWM(11,50)

p.start(0)

duration = 2
pulsems = 500

starttime = time.time()
pulsems = float(pulsems / 1000.)
while(time.time() - starttime < duration):
    p.ChangeDutyCycle(50)
    time.sleep(pulsems)
    p.ChangeDutyCycle(0)
    time.sleep(pulsems)
