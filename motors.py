import time

import RPi.GPIO as GPIO
from math import *

leftMotPwm = None
rightMotPwm = None
stopCall = False
nowTime = None
delayTime = None
refreshTime = 15

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

def fullMotorTimer(time):
	# rightMotPwm.ChangeDutyCycle(0)
	# leftMotPwm.ChangeDutyCycle
	print("oui")

def createDelay(delay, now):
	return time.time() < now + delay


# 200 = Stop
# 201 = Left
# 202 = Forward
# 203 = Right
# 204 = Backward
def adaptDutyCycleDep(camValue):
	global stopCall
	global nowTime

	if camValue != -100 and camValue != 100 and  -100 < camValue < 100:
		stopCall = False

		if camValue < 0:
			leftPow = floor((100 - camValue) /2)
			rightPow = ceil(50 + (camValue / 2))


		elif camValue > 0:
			leftPow = ceil(50 + (camValue / 2))
			rightPow = floor((100 - camValue) /2)

		else:
			leftPow = 50
			rightPow = 50

		print("---------")
		print("VALUE: " + str(camValue))
		print("LEFT: " + str(leftPow))
		print("RIGHT: " + str(rightPow))

		# rightMotPwm.ChangeDutyCycle(rightPow)
		# leftMotPwm.ChangeDutyCycle(leftPow)

	elif camValue >= 200:  # Let assume we need 5sec for a 90° turn and 3sec to be right on the qrcode
		if nowTime is None or nowTime < time.time() - refreshTime:
			nowTime = time.time()

		print(str(nowTime) + " and " + str(nowTime - time.time() + refreshTime))

		# if camValue == 200:  # Stop
		# 	fullMotorTimer(3)
		#
		# elif camValue == 201:  # Left
		# 	fullMotorTimer(3)
		# 	# rightMotPwm.ChangeDutyCycle(0)
		# 	# leftMotPwm.ChangeDutyCycle(100)
		# 	sleep(5)
		#
		# elif camValue == 202:  # Forward
		# 	fullMotorTimer(3)
		#
		# elif camValue == 203:  # Right
		# 	fullMotorTimer(3)
		# 	# rightMotPwm.ChangeDutyCycle(100)
		# 	# leftMotPwm.ChangeDutyCycle(0)
		# 	sleep(5)
		#
		# elif camValue == 204:  # Behind (Should never happen)
		# 	fullMotorTimer(3)
		# 	# rightMotPwm.ChangeDutyCycle(0)
		# 	# leftMotPwm.ChangeDutyCycle(100)
		# 	sleep(10)
		#
		# 	# rightMotPwm.ChangeDutyCycle(0)
		# 	# leftMotPwm.ChangeDutyCycle(0)
		# 	stopCall = False
	else:
		leftPow = 0
		rightPow = 0
		# Maybe add a method to analyze the area

		# rightMotPwm.ChangeDutyCycle(rightPow)
		# leftMotPwm.ChangeDutyCycle(leftPow)

		print("---------")
		print("VALUE: "+ str(camValue))
		print("LEFT: "+ str(leftPow))
		print("RIGHT: "+ str(rightPow))

