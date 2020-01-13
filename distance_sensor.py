import RPi.GPIO as GPIO
import time
import config as cfg

GPIO.setmode(GPIO.BCM)

GPIO.setup(cfg.PIN_TRIG, GPIO.OUT)
GPIO.setup(cfg.PIN_ECHO, GPIO.IN)


def getDistance():
	start = None
	stop = None

	GPIO.output(cfg.PIN_TRIG, True)
	time.sleep(0.00001)
	GPIO.output(cfg.PIN_TRIG, False)

	while GPIO.input(cfg.PIN_ECHO) == 0:
		start = time.time()

	while GPIO.input(cfg.PIN_ECHO) == 1:
		stop = time.time()

	tps = stop - start
	dist = int((tps * 34300) / 2)

	if dist < 1000:
		return dist

