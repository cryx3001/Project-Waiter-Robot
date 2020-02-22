import log

target_id = -1


def get_status_code(t):
	if t is not None:
		global target_id
		target_id = t
		log.debug("GET " + str(target_id))


def send_status_code():
	tab = {
		-3: "Sur cible",
		-2: "Annulé",
		-1: "Attente",
		0: "Retour",
	}

	if target_id > 0:
		return "Go: " + str(target_id)
	else:
		return tab[target_id]


def get_target():
	return target_id
