import csv,serial,datetime,os,time

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
# we are trying to find the key words SATZ,SATA,PASS_UTC
def strMatching(col2find,col2match,place2find):
    strMatch = True
    while strMatch is True:
        for idx, word in enumerate(col2find):
            if word == col2match:
                place2find.append(idx) #stores column place that it found the key word
                strMatch = False

# finds info under key word and adds to the list to hold all the information pertaining to key word
def findInfoUnderCol(col2find,place2find,infoArr):
    notfound = True
    while notfound is True:
        for idx, info in enumerate(col2find):
            if idx == place2find:
                infoArr.append(info) #stores column place that it found the key word
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

#--------------------Parsing IMU and IR sensor values---------------------------
def azimuth(str):
    delimx = str.index("x",0,len(str)-1)
    return float(str[:delimx])

def zenith(str):
    delimx = str.index("x",0,len(str)-1)
    delimy = str.index("y",0,len(str)-1)
    return float(str[delimx:delimy])

def irvalue(str):
    delimy = str.index("y", 0, len(str) - 1)
    return float(str[delimy:])
#---------------End of Parsing IMU and IR sensor values--------------------------

# --------------------Device connection ----------------------------------------
arduinoport1 = "/dev/ttyAMA0"  # receives data from IR sensor and IMU
arduinoport2 = "/dev/ttyAMA1"  # sends data to the Azimuth and Zenith Servos

try:
    s1 = serial.Serial(arduinoport1, 9600)
    s2 = serial.Serial(arduinoport2, 9600)
    if s1.read(10) == 'i':
        ir = s1
    if s1.read(10) == 's':
        ser = s1
    if s2.read(10) == 'i':
        ir = s2
    if s2.read(10) == 's':
        ser = s2
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
            if (PASS_UTC_info[0] - datetime.timedelta(minutes = 8)) == now: # before pass
                #calibrate servos and imu
                ser.write("<c>")
                time.sleep(60)
                #move to desired position
                ser.write("<" + SATA_info[0]+"><"+SATZ_info[0]+">")
                os.system('raspistill -ISO 800 -w 3280 -h 2464 -q 100 -r -ss 5500000 -vf -o /home/pi/Desktop/Pan-Tilt_SYS/Pictures/'+ filename +'before.jpg')
                time.sleep(10)
                #gets IR reading
                IRIMU_bef = str(ir.read(10))
                #gets IMU values
                AZIMUTH_BEF = azimuth(IRIMU_bef)
                ZENITH_BEF = zenith(IRIMU_bef)
                IRVALUE_BEF = irvalue(IRIMU_bef)
                #save in csv
                f.writerow(["before"+PASS_UTC_info[0],IRVALUE_BEF,filename + "before.jpg",AZIMUTH_BEF,ZENITH_BEF])
            if PASS_UTC_info[0] + datetime.timedelta(seconds = 10) == now: # after pass
                #gets IR reading
                IRIMU_aft = str(ir.read(10))
                #gets IMU values
                AZIMUTH_AFT = azimuth(IRIMU_aft)
                ZENITH_AFT = zenith(IRIMU_aft)
                IRVALUE_AFT = irvalue(IRIMU_aft)
                os.system('raspistill -ISO 800 -w 3280 -h 2464 -q 100 -r -ss 5500000 -vf -o /home/pi/Desktop/Pan-Tilt_SYS/Pictures/'+ filename +'after.jpg')
                #save in csv
                f.writerow(["after"+PASS_UTC_info[0],IRVALUE_AFT,filename + "after.jpg",AZIMUTH_AFT,ZENITH_AFT])
                SATZ_info.remove(SATZ[0])
                SATA_info.remove(SATA[0])
                PASS_UTC_info.remove(PASS_UTC_info[0])
                #reset position of the device
                ser.write("<r>")
                time.sleep(20)
                break
#--------------------End of Looping through arrays and saving-------------------