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
  ser.flushInput() # empty buffer.
  ser.write(b'54')
  ser.write(b'\n')
  ser.flushInput() # empty buffer.
  #time.sleep(0.5) # wating for WSN to empty array.
  for i in range(1,34):
    temp = List[i]
    print(temp)
    ser.write(temp.encode())
    ser.write(b'\n')
    time.sleep(0.01)
    ser.flushInput() # empty buffer.
  #time.sleep(0.5)
  print("UART Done.")

# done.