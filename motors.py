import time
import distance_sensor as ds
import RPi.GPIO as GPIO
from math import *
import config as cfg
import log

leftMotPwm = None
rightMotPwm = None
carryMotPwm = None
stopCall = False
sensorCollision = False

def initPwm():
	global leftMotPwm
	leftMotPwm = GPIO.PWM(cfg.PIN_LEFT_MOTOR, 1000)
	leftMotPwm.start(0)

	global rightMotPwm
	rightMotPwm = GPIO.PWM(cfg.PIN_RIGHT_MOTOR, 1000)
	rightMotPwm.start(0)

	global carryMotPwm
	rightMotPwm = GPIO.PWM(cfg.PIN_CARRY_SPEED, 1000)
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
			time.sleep(cfg.TURN_TIME)

		elif camValue == 204:  # Behind (Should never happen)
			# rightMotPwm.ChangeDutyCycle(100)
			# leftMotPwm.ChangeDutyCycle(0)
			time.sleep(cfg.TURN_TIME*2)

		# rightMotPwm.ChangeDutyCycle(0)
		# leftMotPwm.ChangeDutyCycle(0)
		stopCall = False


def preventCollision():
	global stopCall
	global sensorCollision

	# if stopCall is False:
	#
	# 	dist = ds.getDistance("dep")
	# 	if dist is not None and dist < 50:#1 meter
	# 		# rightMotPwm.ChangeDutyCycle(dist)
	# 		# leftMotPwm.ChangeDutyCycle(dist)
	# 		sensorCollision = True
	#
	# 	else:
	# 		sensorCollision = False


def elevationMotors(direction):
	if direction == "up":
		# GPIO.output(cfg.PIN_CARRY_ROTATION_ONE, True)
		# GPIO.output(cfg.PIN_CARRY_ROTATION_TWO, False)
		log.debug("up")

	elif direction == "down":
		# GPIO.output(cfg.PIN_CARRY_ROTATION_ONE, False)
		# GPIO.output(cfg.PIN_CARRY_ROTATION_TWO, True)
		log.debug("down")

	elif direction == "stop":
		# GPIO.output(cfg.PIN_CARRY_ROTATION_ONE, False)
		# GPIO.output(cfg.PIN_CARRY_ROTATION_TWO, False)
		log.debug("stop")

