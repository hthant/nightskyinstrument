import os, datetime

mytime = datetime.datetime.now()
aa = str(int(mytime.strftime('%Y%m%d%H%M%S')))
print(aa)
os.system('raspistill -ISO 800 -w 3280 -h 2464 -q 100 -r -ss 10000 -vf -o /home/pi/Desktop/'+ aa +'bef.jpg')
print(aa)
