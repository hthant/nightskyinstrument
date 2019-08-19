import csv,serial,datetime,os

#--------------------Importing From CSV File-------------------------------------
SATZ = []
SATZ_info = []
SATA = []
SATA_info = []
PASS_UTC = []
PASS_UTC_info = []

listrow = [] # holds string array of col needed to find
listrowFind = [] # holds string array of col of info needed to find

satz = "SATZ";  
sata = "SATA";
pass_utc = "PASS_UTC";

# finds col2find (key word) within the array(col2match) in this instance
# we are tring to find the key words SATZ,SATA,PASS_UTC
def strMatching(col2find,col2match,place2find):
    strMatch = True
    while strMatch is True:
        for idx, word in enumerate(col2find):
            if word == col2match:
                place2find.append(idx) #stores colomn place that it found the key word
                strMatch = False

# finds info under key word and adds to the list to hold all the information pertaining to key word
def findInfoUnderCol(col2find,place2find,infoArr):
    notfound = True
    while notfound is True:
        for idx, info in enumerate(col2find):
            if idx == place2find:
                infoArr.append(info) #stores colomn place that it found the key word
                notfound = False
aa = str(int(mytime.strftime('%Y%m%d%H%M%S')))

with open('/home/pi/Desktop/Pan-Tilt_SYS/prediction.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 7:
            stringRow = ", ".join(row);
            listrow = stringRow.split(', ')
            strMatching(listrow,satz,SATZ)
            strMatching(listrow,sata,SATA)
            strMatching(listrow,pass_utc,PASS_UTC)
            line_count += 1
        if line_count > 7:
            stringRow = ", ".join(row);
            listrowFind = stringRow.split(', ')
            findInfoUnderCol(listrowFind,SATZ[0],SATZ_info)
            findInfoUnderCol(listrowFind,SATA[0],SATA_info)
            findInfoUnderCol(listrowFind,PASS_UTC[0],PASS_UTC_info)
            line_count += 1 
        else:
            line_count += 1
    #print(SATZ_info,SATA_info,PASS_UTC_info)
            
#removing unnecessary data
SATZ_info.remove('SATZ')
SATA_info.remove('SATA')
PASS_UTC_info.remove('PASS_UTC')
#--------------------End of Importing From CSV File-----------------------------

# --------------------Device connection ----------------------------------------
arduinoport1 = "/dev/ttyAMA0"  # receives data from IR sensor and IMU
arduinoport2 = "/dev/ttyAMA1"  # sends data to the Azimuth and Zenith Servos

try:
    s1 = serial.Serial(arduinoport1, 9600)
    s2 = serial.Serial(arduinoport2, 9600)
except:
    print ("Device connection unsuccessful")

# -------------------End of Device connection-----------------------------------

#--------------------Looping through arrays and saving--------------------------
with open ("/home/pi/Desktop/Pan-Tilt_SYS/output.csv","w+") as f: #open file
    f = csv.writer(f,delimiter=",")
    f.writerow(["before/after","IR temperature","Image file name","IMU Azimuth Value", "IMU Zenith Value"])
    while len(PASS_UTC_info)>0:
        while True:
            mytime = datetime.datetime.now()
            now = mytime.strftime('%Y/%m/%d %H:%M:%S')+"(0)"
            filename = str(int(mytime.strftime('%Y%m%d%H%M%S')))
            if (PASS_UTC_info[0] - datetime.timedelta(minutes = 7)) == now: # before pass
                #calibrate servos and imu
                #move to desired position
                s2.write('')
                os.system('raspistill -ISO 800 -w 3280 -h 2464 -q 100 -r -ss 5500000 -vf -o /home/pi/Desktop/Pan-Tilt_SYS/Pictures/'+ filename +'before.jpg')
                #gets IR reading
                IRIMU_bef = s1.read(10)
                strimuir = str(IRIMU_bef)

                #gets IMU values
                #save in csv
                #f.writerow(["before"+PASS_UTC_info[0],])
            if PASS_UTC_info[0] + datetime.timedelta(seconds = 10) == now: # after pass
                #gets IR reading
                #gets IMU values
                IRIMU_aft = s1.read(10)
                os.system('raspistill -ISO 800 -w 3280 -h 2464 -q 100 -r -ss 5500000 -vf -o /home/pi/Desktop/Pan-Tilt_SYS/Pictures/'+ filename +'after.jpg')
                #save in csv
                SATZ_info.remove(SATZ[0])
                SATA_info.remove(SATA[0])
                PASS_UTC_info.remove(PASS_UTC_info[0])
                #reset position of the device
                break
#--------------------End of Looping through arrays and saving-------------------
