import time
import distance_sensor as ds
import RPi.GPIO as GPIO
from math import *
import config as cfg
import log

left_mot_pwm = None
right_mot_pwm = None
elevation_mot_pwm = None
stop_call = False
sensor_collision = False


def init_pwm():
	"""
	Initialize pwm signals for motors
	"""
	global left_mot_pwm
	left_mot_pwm = GPIO.PWM(cfg.PIN_LEFT_MOTOR, 1000)
	left_mot_pwm.start(0)

	global right_mot_pwm
	right_mot_pwm = GPIO.PWM(cfg.PIN_RIGHT_MOTOR, 1000)
	right_mot_pwm.start(0)


def full_motor_timer():
	"""
	Send a continuous signal to the motors
	"""
	# right_mot_pwm.ChangeDutyCycle(100)
	# left_mot_pwm.ChangeDutyCycle(100)
	print("oui")


# 200 = Stop
# 201 = Left
# 202 = Forward
# 203 = Right
# 204 = Backward
def adapt_duty_cycle_dep(cam_value):
	"""
	Adapt the duty cycle for the two pwm signals of the motors, making the robot rotate
	:param cam_value: Coefficient between -100 and 100 (-100 to 0 -> turning on the left ; 0 to 100 -> turning on the right)
	"""
	global stop_call

	if cam_value != -100 and cam_value != 100 and -100 < cam_value < 100:
		if cam_value < 0:
			left_pow = floor(100 - cam_value)
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


def do_turn(id_value):
	"""
	Make the robot turn on a specific angle depending on the parameter.
	:param id_value: Int between 201 and 204 included.
	"""
	global stop_call

	if id_value >= 201:  # Let assume we need 5sec for a 90° turn and 3sec to be right on the qrcode
		stop_call = True
		full_motor_timer()
		time.sleep(3)

		if id_value == 201:  # Left
			# right_mot_pwm.ChangeDutyCycle(0)
			# left_mot_pwm.ChangeDutyCycle(100)
			time.sleep(5)

		elif id_value == 203:  # Right
			# right_mot_pwm.ChangeDutyCycle(100)
			# left_mot_pwm.ChangeDutyCycle(0)
			time.sleep(cfg.TURN_TIME)

		elif id_value == 204:  # Behind (Should never happen)
			# right_mot_pwm.ChangeDutyCycle(100)
			# left_mot_pwm.ChangeDutyCycle(0)
			time.sleep(cfg.TURN_TIME * 2)

		# right_mot_pwm.ChangeDutyCycle(0)
		# left_mot_pwm.ChangeDutyCycle(0)
		stop_call = False


def prevent_collision():
	"""
	Prevent collisions with the robot if something is too close from it
	"""
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
	"""
	Make the motor for the elevation turning in a way or in the other one
	:param direction: "up","down" or "stop"
	"""
	
	if direction == "up":
		# GPIO.output(cfg.PIN_ELEVATION_ROTATION_ONE, True)
		# GPIO.output(cfg.PIN_ELEVATION_ROTATION_TWO, False)
		log.debug("Elevation: Up")

	elif direction == "down":
		# GPIO.output(cfg.PIN_ELEVATION_ROTATION_ONE, False)
		# GPIO.output(cfg.PIN_ELEVATION_ROTATION_TWO, True)
		log.debug("Elevation: Down")

	elif direction == "stop":
		# GPIO.output(cfg.PIN_ELEVATION_ROTATION_ONE, False)
		# GPIO.output(cfg.PIN_ELEVATION_ROTATION_TWO, False)
		log.debug("Elevation: Stop")
