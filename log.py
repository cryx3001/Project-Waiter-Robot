import datetime
import time

start_time = 0
f = open("static/debug.txt", "a")


def start_timer():
	"""Create a timer for log purposes"""

	global start_time
	start_time = time.time()

	debug("---NEW SESSION---")


def debug(txt):
	"""Create a log "log.txt" stored on the device
	:param txt: String to show
	"""

	now = datetime.datetime.now()
	date = "[" + str("{0:02d}".format(now.hour)) + ":" + str("{0:02d}".format(now.minute)) + ":" + str(
		"{0:02d}".format(now.second)) + "]" + "[" + str("{0:6.2f}".format(time.time() - start_time)) + "]"

	text_f = date + " " + txt
	print(text_f)
	f.write(str(text_f) + "\n")
