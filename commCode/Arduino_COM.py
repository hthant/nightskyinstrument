import serial
import time
import csv

#ser = serial.Serial('/dev/ttyACM0',9600)
#ser.flushinout

    #try:
        #ser_val = ser.readline()
        #decoded_val = float(ser_val[0:len(ser_val)-2].decode("utf-8"))
        #print(decoded_val)
with open ("/home/pi/Desktop/Pan-Tilt_SYS/output.csv","w+") as f:
    f = csv.writer(f,delimiter=",")
    f.writerow(["a", "b"])
    f.writerow(["c", "d"])
