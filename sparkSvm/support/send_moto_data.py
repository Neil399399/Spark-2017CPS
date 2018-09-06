import serial
import time
# configuration Serial Port using UART.
try:
  ser = serial.Serial('COM4', 115200)#, timeout=1)
  if ser.isOpen():
    ser.close()
  ser.open()
except:
  pass

# get data
def getList(List):
  #computing List
  try:
    ser.write("54")
    ser.write("\n")
    #time.sleep(0.5) # wating for WSN to empty array.
    for i in range(0,34):
      #time.sleep(0.01)
      temp = List[i]
      print temp
      ser.write(temp)
      ser.write("\n")
    ser.flushInput() # empty buffer.
    #time.sleep(0.5)
  except:
    print "The Uart has being used."
    pass
  finally:
    print "ALL Done."

  #continue

# done.