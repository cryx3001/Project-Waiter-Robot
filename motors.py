import RPi.GPIO as GPIO
from math import *

leftMotPwm = None
rightMotPwm = None

def initMotorsDep(leftPinBcm, rightPinBcm):
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(leftPinBcm)
	GPIO.setup(rightPinBcm)

	global leftMotPwm
	leftMotPwm = GPIO.PWM(leftPinBcm, 1000)
	leftMotPwm.start(0)

	global rightMotPwm
	rightMotPwm = GPIO.PWM(rightPinBcm, 1000)
	rightMotPwm.start(0)


def adaptDutyCycleDep(camValue):
	if camValue != -100 and camValue != 100:
		if camValue < 0:
			leftPow = floor((100 - camValue) /2)
			rightPow = ceil(50 + (camValue / 2))


		elif camValue > 0:
			leftPow = ceil(50 + (camValue / 2))
			rightPow = floor((100 - camValue) /2)

		else:
			leftPow = 50
			rightPow = 50

	else:
		leftPow = 0
		rightPow = 0
		# Maybe add a method to analyze the area

	# rightMotPwm.ChangeDutyCycle(rightPow)
	# leftMotPwm.ChangeDutyCycle(leftPow)

	print("LEFT: "+ str(leftPow))
	print("RIGHT: "+ str(rightPow))

