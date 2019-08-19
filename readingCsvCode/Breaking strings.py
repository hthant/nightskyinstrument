import serial

imu = serial.Serial('/dev/ttyACM0',9600)
#while True:
    #Temp_Read = int(ser.readline())
l = str(imu.readline())
k = l[2:-5]
space = k.index(" ",0,len(k)-1)
sata = int(k[:space-len(k)])/100
satz = int(k[space:])/100
print(sata)
print(satz)
