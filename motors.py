import RPi.GPIO as GPIO

chLeft = 0
chRight = 1

hz = 1000
hLeft = GPIO.PWM(chLeft, hz)
hRight = GPIO.PWM(chRight, hz)

def startPulseModulation(h, dc):
	h.start(dc)

def stopPulseModulation(h):
	h.stop()

def newDutyCyle(h, dc):
	h.ChangeDutyCycle(dc)