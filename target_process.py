import time
target_id = -1

def getStatusCode(t):
	if t is not None:
		global target_id
		target_id = t
		print("GET " + str(target_id))


def sendStatusCode():
		if target_id == -3:
			return "Sur cible"
		elif target_id == -2:
			return "Annulé"
		elif target_id == -1:
			return "Attente"
		elif target_id == 0:
			return "Retour"
		elif target_id > 0:
			return "Go: " + str(target_id)

