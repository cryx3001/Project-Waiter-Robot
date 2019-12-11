import time
target_id = -1

def getStatusCode(t):
	if t is not None:
		global target_id
		target_id = t
		print("GET " + str(target_id))


def sendStatusCode():
	while True:
		time.sleep(1)
		print("SENT")
		yield str(target_id)

