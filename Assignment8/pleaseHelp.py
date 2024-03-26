import time
import serial
try:
    ser = serial.Serial()
    ser.port = '/dev/ttyUSB0'
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS 
    ser.parity =serial.PARITY_NONE 
    ser.stopbits = serial.STOPBITS_ONE 
    ser.timeout = 1
    ser.open()
    # ser.write(b'\r\r')
    time.sleep(1)
    # ser.write(b'lep\r')
    ser.close()
except Exception as e:
    print(e)
    pass
# print(ser)

ser.open()

while True:
    try:
        data=str(ser.readline())
        print(data)
        time.sleep(0.01)
        break
    except Exception as e:
        print(e)
        pass
    except KeyboardInterrupt:
        ser.close()
