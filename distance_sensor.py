import RPi.GPIO as GPIO
import time
import config as cfg
import log


def get_distance(type_sensor):
	"""
	Get the distance between the sensor and the obstacle
	:param type_sensor: "dep" or "elev", depending of the sensor chose
	:return: The distance in centimeters
	"""

	start = None
	stop = None

	tab_sensors = {
		"dep": (cfg.PIN_TRIG, cfg.PIN_ECHO),
		"elev": (cfg.PIN_TRIG_ELEVATION, cfg.PIN_ECHO_ELEVATION)
	}

	trig = tab_sensors[type_sensor][0]
	echo = tab_sensors[type_sensor][1]

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
