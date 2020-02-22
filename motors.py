import time
import distance_sensor as ds
import RPi.GPIO as GPIO
from math import *
import config as cfg
import log

left_mot_pwm = None
right_mot_pwm = None
carry_mot_pwm = None
stop_call = False
sensor_collision = False


def init_pwm():
	global left_mot_pwm
	left_mot_pwm = GPIO.PWM(cfg.PIN_LEFT_MOTOR, 1000)
	left_mot_pwm.start(0)

	global right_mot_pwm
	right_mot_pwm = GPIO.PWM(cfg.PIN_RIGHT_MOTOR, 1000)
	right_mot_pwm.start(0)

	global carry_mot_pwm
	right_mot_pwm = GPIO.PWM(cfg.PIN_CARRY_SPEED, 1000)
	right_mot_pwm.start(0)


def full_motor_timer():
	# right_mot_pwm.ChangeDutyCycle(100)
	# left_mot_pwm.ChangeDutyCycle(100)
	print("oui")


# 200 = Stop
# 201 = Left
# 202 = Forward
# 203 = Right
# 204 = Backward
def adapt_duty_cycle_dep(cam_value):
	global stop_call

	if cam_value != -100 and cam_value != 100 and -100 < cam_value < 100:
		if cam_value < 0:
			left_pow = floor(100 + cam_value)
			right_pow = 100


		elif cam_value > 0:
			left_pow = 100
			right_pow = floor(100 - cam_value)

		else:
			left_pow = 100
			right_pow = 100

	else:
		left_pow = 0
		right_pow = 0


# right_mot_pwm.ChangeDutyCycle(right_pow)
# left_mot_pwm.ChangeDutyCycle(left_pow)


def do_turn(cam_value):
	global stop_call

	if cam_value >= 200:  # Let assume we need 5sec for a 90° turn and 3sec to be right on the qrcode
		stop_call = True
		full_motor_timer()
		time.sleep(3)

		if cam_value == 201:  # Left
			# right_mot_pwm.ChangeDutyCycle(0)
			# left_mot_pwm.ChangeDutyCycle(100)
			time.sleep(5)

		elif cam_value == 203:  # Right
			# right_mot_pwm.ChangeDutyCycle(100)
			# left_mot_pwm.ChangeDutyCycle(0)
			time.sleep(cfg.TURN_TIME)

		elif cam_value == 204:  # Behind (Should never happen)
			# right_mot_pwm.ChangeDutyCycle(100)
			# left_mot_pwm.ChangeDutyCycle(0)
			time.sleep(cfg.TURN_TIME * 2)

		# right_mot_pwm.ChangeDutyCycle(0)
		# left_mot_pwm.ChangeDutyCycle(0)
		stop_call = False


def prevent_collision():
	global stop_call
	global sensor_collision


# if stop_call is False:
#
# 	dist = ds.get_distance("dep")
# 	if dist is not None and dist < 50:#1 meter
# 		# right_mot_pwm.ChangeDutyCycle(dist)
# 		# left_mot_pwm.ChangeDutyCycle(dist)
# 		sensor_collision = True
#
# 	else:
# 		sensor_collision = False


def elevation_motors(direction):
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
