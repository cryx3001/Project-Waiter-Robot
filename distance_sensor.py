import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIN_TRIG = 26
PIN_ECHO = 20

GPIO.setup(PIN_TRIG, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)


def getDistance():
	start = None
	stop = None

	GPIO.output(PIN_TRIG, True)
	time.sleep(0.00001)
	GPIO.output(PIN_TRIG, False)

	while GPIO.input(PIN_ECHO) == 0:
		start = time.time()

	while GPIO.input(PIN_ECHO) == 1:
		stop = time.time()

	tps = stop - start
	dist = int((tps * 34300) / 2)

	if dist < 1000:
		return dist

