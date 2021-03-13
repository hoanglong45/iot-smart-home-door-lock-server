from flask import Blueprint, request, jsonify, Response
import cv2
import numpy as np

bp_recognition = Blueprint('recognition', __name__)

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('models/model.yml')
font = cv2.FONT_HERSHEY_SIMPLEX

ids = 0
names = ['None', 'Long']


class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(3, 640)
        self.video.set(4, 480)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        min_width = 0.1 * self.video.get(3)
        max_width = 0.1 * self.video.get(4)
        ret, image = self.video.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(min_width), int(max_width))
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            ids, confidence = recognizer.predict(roi_gray)
            print(str(ids) + " => " + str(confidence))
            if (confidence < 100):
                ids = names[ids]
                print('ids', ids)
                confidence = " {0}".format(round(100 - confidence))
            else:
                ids = "unknown"
                confidence = " {0}".format(round(100 - confidence))

            cv2.putText(image, str(ids), (x + 5, y - 5),
                        font, 1, (255, 255, 255), 2)
            cv2.putText(image, str(confidence), (x + 5, y + h - 5),
                        font, 1, (255, 255, 0), 1)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@bp_recognition.route('/api/recognition')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')
