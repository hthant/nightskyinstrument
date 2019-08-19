import serial
import csv

ser = serial.Serial('/dev/ttyACM1',9600, timeout = 2)


while 1:
   ir_vals = ser.readline().decode('ascii')
   print (ir_vals)
    
with open ('/home/pi/Desktop/IRvals.csv', 'w+' ) as csv_writer:
        fieldnames = ['Celcius','Faernheit']
        
        csv_writer = csv.DictWriter(csv_writer, fieldnames = fieldnames, delimiter=',')
            
        csv_writer.writeheader()
        csv_writer.writerow(ir_vals)
