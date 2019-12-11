from imutils.video import WebcamVideoStream
from flask import Response, Flask, render_template, request, jsonify
import threading
import cv2
import argparse

import target_process as tp
import stream_process as sp

vs = WebcamVideoStream(src=0).start()
lock = threading.Lock()
app = Flask(__name__)
parser = argparse.ArgumentParser()
parser.add_argument("--stream", help="Send video feedback.", action="store_true")
args = parser.parse_args()
numberTable = None

def main():
	img = vs.read()

	img = img[0:int(img.shape[0] / 2), 100:(img.shape[1] - 100)]
	height, width, channels = img.shape

	qrText = sp.detect_qrcode(img, args.stream)

	if not qrText:
		img, biggest_contour, cX, cY = sp.process_contours(img, args.stream)
		#print(sp.send_order_direction(100, width, cX))

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


@app.route("/")
def index():
	print("RENDER")
	return render_template("index.html")


@app.route("/video_feed")
def video_feed():
	return Response(show_webcam(), mimetype="multipart/x-mixed-replace; boundary=frame")

#  1-99	: Go to target number ..
#  0	: Go to home
# -1 	: Nothing sent
# -2 	: Action cancelled
# -3 	: Timeout error
@app.route('/api_send', methods=["POST"])
def getStatus():
	if request.method == "POST":
		try:
			numberTable = request.values.get('input', '')
			tp.getStatusCode(int(numberTable))
			return numberTable

		except ValueError:
			tp.getStatusCode(-1)
			return -1


@app.route('/api_get')
def sendStatus():
	return Response(tp.sendStatusCode())

if __name__ == '__main__':
	app.run("0.0.0.0", "8000", debug=True, threaded=True, use_reloader=False)