from flask import Blueprint, Response
import cv2
from firebase import Firebase

config = {
    "apiKey": "AIzaSyCfTKQ-5sDNvN3QfC6S4oqeKOnbEv7AxzE",
    "authDomain": "iot-smart-home-door-lock-7ccc9.firebaseapp.com",
    "databaseURL": "https://iot-smart-home-door-lock-7ccc9.firebaseio.com",
    "projectId": "iot-smart-home-door-lock-7ccc9",
    "storageBucket": "iot-smart-home-door-lock-7ccc9.appspot.com",
    "messagingSenderId": "513607106040",
    "appId": "1:513607106040:web:d627644390357454e76a0d"
}

bp_recognition = Blueprint('recognition', __name__)
firebase = Firebase(config)
db = firebase.database()
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('models/model.yml')
font = cv2.FONT_HERSHEY_SIMPLEX

rfid = 0


def get_user_by_rfid(rfid):
    all_users = db.child('Users').get()
    for user in all_users.each():
        if rfid == user.val()['rfid']:
            name = user.val()['name']
            return name


def recognition():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while cap.isOpened():
        ret, image = cap.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        if ret:
            for (x, y, w, h) in face_rects:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                rfid, confidence = recognizer.predict(roi_gray)
                print(str(rfid) + " => " + str(confidence))
                if(confidence <= 25):
                    name = get_user_by_rfid(str(rfid))
                    print('name', name)
                    confidence = " {0}".format(round(100 - confidence))

                else:
                    rfid = 'unknown'
                    confidence = " {0}".format(round(100 - confidence))

                cv2.putText(image, str(rfid), (x + 5, y - 5),
                            font, 1, (255, 255, 255), 2)
                cv2.putText(image, str(confidence), (x + 5, y + h - 5),
                            font, 1, (255, 255, 0), 1)
            frame = cv2.imencode('.jpg', image)[1].tobytes()
            yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'

        else:
            break

    cap.release()


@bp_recognition.route('/api/recognition')
def video_feed():
    return Response(recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')
