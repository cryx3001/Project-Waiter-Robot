import log

target_id = -1


#  > 0	: Go to target number ..
#  0	: Go to home
# -1 	: Nothing sent
# -2	: On Target
# -3	: Stopped

def get_status_code(t):
	"""
	Storing the input of the user
	:param t: The input from the webpage
	"""
	if t is not None:
		global target_id
		target_id = t
		log.debug("GET " + str(target_id))


def send_status_code():
	"""
	Make the codes readable by the user
	:return: The redable version of the code
	"""
	tab_code = {
		-3: "Stopped",
		-2: "On target",
		-1: "Waiting for input",
		0: "Going home",
	}

	if target_id > 0:
		return "Go: " + str(target_id)
	else:
		return tab_code[target_id]


def get_target():
	"""
	:return: Get target_id
	"""
	return target_id
