import time

import RPi.GPIO as GPIO
from math import *

leftMotPwm = None
rightMotPwm = None
stopCall = False
turnTime = 5

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


def fullMotorTimer():
	# rightMotPwm.ChangeDutyCycle(100)
	# leftMotPwm.ChangeDutyCycle(100)
	print("oui")


# 200 = Stop
# 201 = Left
# 202 = Forward
# 203 = Right
# 204 = Backward
def adaptDutyCycleDep(camValue):
	global stopCall

	if camValue != -100 and camValue != 100 and -100 < camValue < 100:
		if camValue < 0:
			leftPow = floor(100 + camValue)
			rightPow = 100


		elif camValue > 0:
			leftPow = 100
			rightPow = floor(100 - camValue)

		else:
			leftPow = 100
			rightPow = 100

		# rightMotPwm.ChangeDutyCycle(rightPow)
		# leftMotPwm.ChangeDutyCycle(leftPow)

	else:
		leftPow = 0
		rightPow = 0
		# Maybe add a method to analyze the area

		# rightMotPwm.ChangeDutyCycle(rightPow)
		# leftMotPwm.ChangeDutyCycle(leftPow)


def doTurn(camValue):
	global stopCall

	if camValue >= 200:  # Let assume we need 5sec for a 90° turn and 3sec to be right on the qrcode
		stopCall = True
		fullMotorTimer()
		time.sleep(3)

		if camValue == 201:  # Left
			# rightMotPwm.ChangeDutyCycle(0)
			# leftMotPwm.ChangeDutyCycle(100)
			time.sleep(5)

		elif camValue == 203:  # Right
			# rightMotPwm.ChangeDutyCycle(100)
			# leftMotPwm.ChangeDutyCycle(0)
			time.sleep(5)

		elif camValue == 204:  # Behind (Should never happen)
			# rightMotPwm.ChangeDutyCycle(100)
			# leftMotPwm.ChangeDutyCycle(0)
			time.sleep(10)

		# rightMotPwm.ChangeDutyCycle(0)
		# leftMotPwm.ChangeDutyCycle(0)

		stopCall = False