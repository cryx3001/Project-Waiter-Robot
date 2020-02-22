import datetime
import time

start_time = 0


def start_timer():
	global start_time
	start_time = time.time()


def debug(txt):
	now = datetime.datetime.now()
	date = "[" + str("{0:02d}".format(now.hour)) + ":" + str("{0:02d}".format(now.minute)) + ":" + str(
		"{0:02d}".format(now.second)) + "]" + "[" + str("{0:6.2f}".format(time.time() - start_time)) + "]"

	print(date, str(txt))
