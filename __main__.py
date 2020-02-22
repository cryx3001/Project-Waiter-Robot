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
	global i
	i = i + 1

	img = vs.read()
	img = img[0:int(img.shape[0] / 2), 100:(img.shape[1] - 100)]

	qr_text = sp.detect_qrcode(img, args.stream)
	if not qr_text:
		img, biggest_contour, c_x, c_y = sp.process_contours(img, args.stream)

		if i >= 5:
			sp.send_order_direction(100, img.shape[1], c_x)
			i = 0

	status_text = tp.send_status_code()
	cv2.putText(img, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (155, 155, 155), 2)

	return img


def show_webcam():
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
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(cfg.PIN_LEFT_MOTOR, GPIO.OUT)
	GPIO.setup(cfg.PIN_RIGHT_MOTOR, GPIO.OUT)
	mot.init_pwm()

	GPIO.setup(cfg.PIN_TRIG, GPIO.OUT)
	GPIO.setup(cfg.PIN_ECHO, GPIO.IN)

	GPIO.setup(cfg.PIN_TRIG_ELEVATION, GPIO.OUT)
	GPIO.setup(cfg.PIN_ECHO_ELEVATION, GPIO.IN)

	GPIO.setup(cfg.PIN_CARRY_SPEED, GPIO.OUT)
	GPIO.setup(cfg.PIN_CARRY_ROTATION_ONE, GPIO.OUT)
	GPIO.setup(cfg.PIN_CARRY_ROTATION_TWO, GPIO.OUT)


@app.route("/")
def index():
	log.debug("RENDER")
	return render_template("index.html")


@app.route("/video_feed")
def video_feed():
	return Response(show_webcam(), mimetype="multipart/x-mixed-replace; boundary=frame")


#  > 0	: Go to target number ..
#  0	: Go to home
# -1 	: Nothing sent
# -2 	: Action cancelled
# -3	: On Target
@app.route('/api', methods=["POST"])
def get_status():
	if request.method == "POST":
		try:
			number_table = request.values.get('input', '')
			tp.get_status_code(int(number_table))
			return number_table

		except ValueError:
			tp.get_status_code(-1)
			return -1


if __name__ == '__main__':
	log.start_timer()
	app.run("0.0.0.0", "8000", debug=True, threaded=True, use_reloader=False)

GPIO.cleanup()
