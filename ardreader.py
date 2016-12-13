import serial
import io
ser = serial.Serial('/dev/ttyACM1')
while(1):
  s = ser.readline()
  s = s.split()
  print int(s[0])
  ser.flush()
