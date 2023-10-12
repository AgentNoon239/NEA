import time
import os
import glob

import cv2

f = open("data.csv","a+")

cam = cv2.VideoCapture(0)
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def get_temp_file():
	with open(device_file,"r") as f:
		return f.readlines()

while True:
	while True:
		lines = get_temp_file()
		if lines[0].strip()[-3:] == "YES":
			break
			
		time.sleep(0.2)

	temp_pos = lines[1].find("t=")
	temp = float(lines[1][temp_pos+2:]) / 1000

	f.writelines([f"{time.ctime()}, {temp}"])
	f.flush()

	ret, frame = cam.read()

	if ret:
		cv2.imwrite(f"imgs/{time.ctime()}.png",frame)

	time.sleep(3600)	