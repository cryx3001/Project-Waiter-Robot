import time
import distance_sensor as ds
import target_process as tp
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


def adapt_duty_cycle_dep(cam_value):
	"""
	Adapt the duty cycle for the two pwm signals of the motors, making the robot rotate
	:param cam_value: Coefficient between -100 and 100 (-100 to 0 -> turning on the left ; 0 to 100 -> turning on the right)
	"""
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


# log.debug("LEFT: " + str(left_pow) + " | RIGHT: " + str(right_pow))


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
		log.debug("Node step started. Going on qr code.")
		time.sleep(3)

		tab_motors = {
			201: (0, 100, cfg.TURN_TIME),  # Left
			202: (100, 100, cfg.TURN_TIME),  # Forward
			203: (100, 0, cfg.TURN_TIME),  # Right
			204: (100, 0, cfg.TURN_TIME * 2)  # Backward
		}

		log.debug(
			str(id_value) + ": " + str(tab_motors[id_value][0]) + " " + str(tab_motors[id_value][1]) + " "
			+ str(tab_motors[id_value][2])
		)

		# right_mot_pwm.ChangeDutyCycle(tab_motors[id_value][0])
		# left_mot_pwm.ChangeDutyCycle(tab_motors[id_value][1])
		time.sleep(tab_motors[id_value][2])
		log.debug("Node step finished")

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


def elevation():
	"""
	For when the robot has to give the plates
	"""

	# Let's assume for the moment that the "arms" are on their highest level
	# We have to time how much time does it take to lower the arms, then they will raise for the same amount of time
	global stop_call
	stop_call = True
	tp.get_status_code(-2)
	elevation_motors("down")
	
	time_start = time.time()

	while True:
		if ds.get_distance("elev") < 5:
			elevation_motors("stop")
			time_needed = time.time() - time_start
			log.debug("Time needed: " + str(time_needed))
			break

	# Then the arms doesn't move for 10 seconds, giving the time for the users to take the plates
	while True:
		if (time_needed + time_start + cfg.PAUSE_TIME) < time.time():
			elevation_motors("up")
			break

	time_start = time.time()
	log.debug("Motor should stop at " + str(time_start + time_needed))
	while True:
		if time.time() > (time_start + time_needed):
			elevation_motors("stop")
			log.debug("Stopped at " + str(time.time()))
			break

	do_turn(204)  # The robot will do a 180° turn, and then will go back to "home"
	tp.get_status_code(0)


def elevation_motors(direction):
	"""
	Make the motor for the elevation turning in a way or in the other one
	:param direction: "up","down" or "stop"
	"""

	tab_elev = {
		"up": (True, False, "Up"),
		"down": (False, True, "Down"),
		"stop": (False, False, "Stop"),
	}

	# GPIO.output(cfg.PIN_ELEVATION_ROTATION_ONE, tab[direction][0])
	# GPIO.output(cfg.PIN_ELEVATION_ROTATION_TWO, tab[direction][1])
	log.debug("Elevation: " + str(tab_elev[direction][2]))
