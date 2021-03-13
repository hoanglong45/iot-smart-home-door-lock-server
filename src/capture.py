import cv2
import time
from flask import Blueprint, Response

bp_capture = Blueprint('capture', __name__)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
count = 0
ds_factor = 0.6


class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        global count
        ret, image = self.video.read()
        image = cv2.resize(image, None, fx=ds_factor,
                           fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in face_rects:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            count += 1
            cv2.imwrite("dataset/user." + "1." +
                        str(count) + ".jpg", roi_gray)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def gen(camera):
    while True:
        if count < 30:
            frame = camera.get_frame()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            time.sleep(0.2)


@bp_capture.route('/api/capture')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')
