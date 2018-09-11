import serial
import time
# configuration Serial Port using UART.
ser = serial.Serial('COM4', 115200, timeout=1)

if ser.isOpen():
  ser.close()
ser.open()

# get data

def getList(List):
  #computing List
  ser.write("54")
  ser.write("\n")
  #time.sleep(0.5) # wating for WSN to empty array.
  for i in range(0,34):
    temp = List[i]
    print temp
    ser.write(temp)
    ser.write("\n")
  ser.flushInput() # empty buffer.
  #time.sleep(0.5)
  print "UART Done."

# done.