import time
import os
import glob
import getpass

device = "pi"
pi_camera = device == "pi"

if pi_camera:
	from picamera2 import Picamera2
	picam2 = Picamera2()
	picam2.start(show_preview=False)
else:
	import cv2
	cam = cv2.VideoCapture(0)

f = open("data.csv","a+")

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def get_temp_file():
	with open(device_file,"r") as f:
		return f.readlines()

count = 0
while True:
	while True:
		lines = get_temp_file()
		if lines[0].strip()[-3:] == "YES":
			break
			
		time.sleep(0.2)

	temp_pos = lines[1].find("t=")
	temp = float(lines[1][temp_pos+2:]) / 1000

	print(temp)
	f.writelines([f"{time.ctime()}, {temp}"])
	f.flush()

	if count % 6 == 0:
		if pi_camera:
			try: 
				picam2.capture_file(f"imgs/{time.ctime()}.png")
			except:
				print(False)
			else:
				print(True)

		else:
			ret, frame = cam.read()

			print(ret)
			if ret:
				cv2.imwrite(f"imgs/{time.ctime()}.png",frame)

	count += 1
	time.sleep(600)	