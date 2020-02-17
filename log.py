import datetime
import time

startTime = 0


def startTimer():
	global startTime
	startTime = time.time()


def debug(txt):
	now = datetime.datetime.now()
	date = "[" + str("{0:02d}".format(now.hour)) + ":" + str("{0:02d}".format(now.minute)) + ":" \
			+ str("{0:02d}".format(now.second)) + "]" + "[" + str("{0:6.2f}".format(time.time() - startTime)) + "]"


	print(date, str(txt))
