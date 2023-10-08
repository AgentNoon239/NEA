from gpiozero import MCP3008

f = open("calibration.csv","a+")

temp_sensor = MCP3008(0)

while True:
	t = float(input())
	f.writelines([f"{temp_sensor.value}, {t}"])
	f.flush()