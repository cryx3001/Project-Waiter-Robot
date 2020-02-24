from imutils.video import WebcamVideoStream
from flask import Response, Flask, render_template, request
import threading
import cv2
import argparse
import RPi.GPIO as GPIO
import target_process as tp
import stream_process as sp
import motors as mot
import config as cfg
import log as log

vs = WebcamVideoStream(src=0).start()
lock = threading.Lock()
app = Flask(__name__)
parser = argparse.ArgumentParser()
parser.add_argument("--stream", help="Send video feedback.", action="store_true")
args = parser.parse_args()
number_table = None
i = 0


def main():
	"""Main function"""

	global i
	i = i + 1

	img = vs.read()
	img = img[0:int(img.shape[0] / 2), 100:(img.shape[1] - 100)]
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	if tp.get_target() >= 0:
		qr_text = sp.detect_qrcode(img, args.stream)
		if not qr_text:
			c_x = sp.process_contours(img, args.stream)

			if i >= 5:  # For performance purposes
				sp.send_order_direction(100, img.shape[1], c_x)
				i = 0

	status_text = tp.send_status_code()
	cv2.putText(img, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (155, 155, 155), 2)

	return img


def show_webcam():
	"""Function used to show what's going on with the entire algorithm. (Reduce performances)"""

	missing_img = cv2.imread('./static/img/missing.png')

	while True:
		if args.stream:
			img = main()
		else:
			img = missing_img
			main()

		with lock:
			if img is None:
				continue

			(flag, img) = cv2.imencode(".jpg", img)

			if not flag:
				continue

		yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(img) + b'\r\n'


def init_pins():
	"""Initialize every pins needed depending on the values in cfg.py"""

	GPIO.setmode(GPIO.BCM)

	GPIO.setup(cfg.PIN_LEFT_MOTOR, GPIO.OUT)
	GPIO.setup(cfg.PIN_RIGHT_MOTOR, GPIO.OUT)
	mot.init_pwm()

	GPIO.setup(cfg.PIN_TRIG, GPIO.OUT)
	GPIO.setup(cfg.PIN_ECHO, GPIO.IN)

	GPIO.setup(cfg.PIN_TRIG_ELEVATION, GPIO.OUT)
	GPIO.setup(cfg.PIN_ECHO_ELEVATION, GPIO.IN)

	GPIO.setup(cfg.PIN_ELEVATION_ROTATION_ONE, GPIO.OUT)
	GPIO.setup(cfg.PIN_ELEVATION_ROTATION_TWO, GPIO.OUT)


@app.route("/")
def index():
	"""Create the web page for the user interface"""

	log.debug("RENDER")
	return render_template("index.html")  # templates/index.html


@app.route("/video_feed")
def video_feed():
	"""Return the video feed"""

	return Response(show_webcam(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/api', methods=["POST"])
def get_status():
	"""
	Return the input from the web page.
	"""

	if request.method == "POST":
		try:
			table_number = request.values.get('input', '')
			tp.get_status_code(int(table_number))

		except ValueError:
			tp.get_status_code(-1)


if __name__ == '__main__':
	log.start_timer()
	app.run("0.0.0.0", "8000", debug=True, threaded=True, use_reloader=False)

GPIO.cleanup()
