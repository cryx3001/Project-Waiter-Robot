import RPi.GPIO as GPIO
import time
import config as cfg
import log

def getDistance(typeSensor):
	start = None
	stop = None

	if typeSensor == "dep":
		trig = cfg.PIN_TRIG
		echo = cfg.PIN_ECHO
	elif typeSensor == "elev":
		trig = cfg.PIN_TRIG_ELEVATION
		echo = cfg.PIN_ECHO_ELEVATION

	GPIO.output(trig, True)
	time.sleep(0.00001)
	GPIO.output(trig, False)

	while GPIO.input(echo) == 0:
		start = time.time()

	while GPIO.input(echo) == 1:
		stop = time.time()

	tps = stop - start
	dist = int((tps * 34300) / 2)

	if dist < 1000:
		return dist
