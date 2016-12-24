import serial
import io
from datetime import datetime, date, time
import time
import numpy as np
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
maxread = 1023
arraysize = 100
avgsum = 0.0
avg = 0
samples = np.zeros(arraysize)
index = 0
		
def sample():
  global avgsum, index
  #time.sleep(100.0 / 1000.0)
  t = str(datetime.time(datetime.now()))
  s = ser.readline().strip('\0').strip().split()
  if len(s) != 0 and '\\' not in s:
    try:
      s = int((s[0]))
    except ValueError:
      sample() #just retry in event of bad serial read
    if s <= maxread:
		avgsum -= samples[index]
		samples[index] = s
		avgsum += samples[index]
		index += 1
		if index > (arraysize - 1):
		  index = 0
		avg = avgsum / arraysize
		print t + "," + str(s) + "," + str(avg)

def simplesample(): 
  print ser.readline().strip('\0').strip()

while(True):
  #simplesample()
  sample()
