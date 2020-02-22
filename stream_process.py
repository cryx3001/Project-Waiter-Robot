import numpy as np
from pyzbar import pyzbar
from threading import Thread
import cv2
import motors as mot
import target_process as tp
import log as log

last_qr_text = None


def detect_qrcode(img, show):
	global last_qr_text

	codes = pyzbar.decode(img)
	qr_text = None

	try:
		if len(codes) > 0:
			for code in codes:
				qr_text = code.data.decode("utf-8")

				if qr_text != last_qr_text:
					get_node_direction(qr_text, tp.get_target())

				last_qr_text = qr_text

				if show:
					points = code.polygon

					pt1 = (min(points[0][0], points[2][0]), min(points[0][1], points[2][1]))
					pt2 = (max(points[0][0], points[2][0]), max(points[0][1], points[2][1]))

					cv2.rectangle(img, pt1, pt2, (25, 25, 25), 2)
					# pt1 en haut a gauche
					# pt2 en bas a droite

					cv2.putText(img, qr_text, (pt1[0], pt1[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (25, 25, 25), 2)

			return qr_text

	except IndexError:
		print("Erreur")


def get_node_direction(qrtext, target):
	data = qrtext.split("/")
	for d in data:
		data_bis = d.split()

		try:
			for d_bis in data_bis:
				if int(d_bis) == target:
					id_turn = data.index(d)

					if not mot.stop_call and not mot.sensor_collision:
						log.debug("ID:" + str(id_turn))
						t = Thread(target=mot.do_turn, args=[201 + id_turn])
						t.start()
					break

		except ValueError:
			log.debug("QR CODE INVALIDE")


def process_contours(img, show):
	gris = np.array([30, 30, 30], dtype="uint8")
	noir = np.array([0, 0, 0], dtype="uint8")

	biggest_contour = None
	mask = 255 - cv2.inRange(img, noir, gris)
	ret, tresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY_INV)
	contours = cv2.findContours(tresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

	if len(contours) > 0:
		for c in contours:
			if biggest_contour is None:
				biggest_contour = c

			if cv2.contourArea(c) > cv2.contourArea(biggest_contour):
				biggest_contour = c

		if show:
			img = cv2.drawContours(img, biggest_contour, -1, (0, 255, 0), 3)

		m = cv2.moments(biggest_contour)

		if m["m10"] != 0 and m["m00"] != 0 and m["m01"] != 0:
			c_x = int(m["m10"] / m["m00"])
			c_y = int(m["m01"] / m["m00"])

			if c_x != 219 and c_y != 119 and show:
				img = cv2.circle(img, (c_x, c_y), 7, (255, 255, 255), -1)

			return img, biggest_contour, c_x, c_y

		else:
			return img, biggest_contour, 0, 0

	else:
		return img, 0, 0, 0


def send_order_direction(xmargin, imgwidth, cx):
	xcenter_img = imgwidth / 2

	xlimit_left = xcenter_img - (xmargin / 2)
	xlimit_right = xcenter_img + (xmargin / 2)

	# print("--------")
	# print("WIDTH " + str(imgwidth))
	# print("CENTER " + str(xcenter_img))
	# print("cx "+ str(cx))
	# print("RIGHT "+ str(xlimit_right))
	# print("LEFT "+ str(xlimit_left))

	if cx < xlimit_left:
		coeff = cx / xlimit_left - 1

	elif cx > xlimit_right:
		coeff = (cx - xlimit_right) / (imgwidth - xlimit_right)

	else:
		coeff = 0

	mot.prevent_collision()  # We have to check if nothing is blocking the robot

	if not mot.stop_call and not mot.sensor_collision:
		mot.adapt_duty_cycle_dep(int(coeff * 100))

# coeff < 0 -> Go left
# coeff > 0 -> Go right
