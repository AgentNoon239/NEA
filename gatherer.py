import time
import cv2
import math 
from scipy import optimize

from gpiozero import MCP3008

f = open("data.csv","a+")

with open("calibration.csv") as f:
	xdata, ydata =zip(*[map(float,i.split(",")) for i in f.read().splitlines()])

cam = cv2.VideoCapture(0)

def convert_to_temp(v,a,b):
	R2 = 10000.0 / ((1023.0 / v) - 1.0);
	v = R2 / 10000.0;
	v = math.log(v) / a
	v = v + 1.0 / (25.0 + 273.15);
	v = (1.0 / v) - 273.15; 
	return v + b

params, _ = optimize.curve_fit(convert_to_temp,xdata,ydata,[3950,0])

temp_sensor = MCP3008(0)

while True:
	v = temp_sensor.value
	t = convert_to_temp(v,*params)
	f.writelines([f"{time.ctime()}, {v}, {t}"])
	f.flush()

	ret, frame = cam.read()

	if ret:
		cv2.imwrite(f"imgs/{time.ctime()}.png",frame)

	time.sleep(3600)	