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
numberTable = None
i = 0

def main():
	global i
	i = i + 1

	img = vs.read()
	img = img[0:int(img.shape[0] / 2), 100:(img.shape[1] - 100)]

	qrText = sp.detect_qrcode(img, args.stream)
	if not qrText:
		img, biggest_contour, cX, cY = sp.process_contours(img, args.stream)

		if i >= 5:
			sp.send_order_direction(100, img.shape[1], cX)
			i = 0

	statusText = tp.sendStatusCode()
	cv2.putText(img, statusText, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (155, 155, 155), 2)

	return img


def show_webcam():
	missingImg = cv2.imread('./static/img/missing.png')

	while True:
		if args.stream:
			img = main()
		else:
			img = missingImg
			main()

		with lock:
			if img is None:
				continue

			(flag, img) = cv2.imencode(".jpg", img)

			if not flag:
				continue


		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(img) + b'\r\n')


def initPins():
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(cfg.PIN_LEFT_MOTOR)
	GPIO.setup(cfg.PIN_RIGHT_MOTOR)
	mot.initPwm()

	GPIO.setup(cfg.PIN_TRIG, GPIO.OUT)
	GPIO.setup(cfg.PIN_ECHO, GPIO.IN)


@app.route("/")
def index():
	print("RENDER")
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
def getStatus():
	if request.method == "POST":
		try:
			numberTable = request.values.get('input', '')
			tp.getStatusCode(int(numberTable))
			return numberTable

		except ValueError:
			tp.getStatusCode(-1)
			return -1


if __name__ == '__main__':
	log.startTimer()
	app.run("0.0.0.0", "8000", debug=True, threaded=True, use_reloader=False)



GPIO.cleanup()
