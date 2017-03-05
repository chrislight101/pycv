import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.OUT) #in1
GPIO.setup(12, GPIO.OUT) #in2
GPIO.setup(13, GPIO.OUT) #in3
GPIO.setup(15, GPIO.OUT) #in4

#left and right motor forward, back, and stop functions
def Lfwd():
    GPIO.output(11, 1)
    GPIO.output(12, 0)
    
def Lbk():
    GPIO.output(11, 0)
    GPIO.output(12, 1)

def Lstp():
    GPIO.output(11, 0)
    GPIO.output(12, 0)
    
def Rfwd():
    GPIO.output(13, 1)
    GPIO.output(15, 0)
    
def Rbk():
    GPIO.output(13, 0)
    GPIO.output(15, 1)

def Rstp():
    GPIO.output(13, 0)
    GPIO.output(15, 0)
    
def Lturn():
    GPIO.output(18, 1)

def Rturn():
    GPIO.output(18, 0)