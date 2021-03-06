from flask import Blueprint, jsonify
import cv2
import os
import numpy as np
from PIL import Image
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

bp_training = Blueprint('training', __name__)
firebase = Firebase(config)
storage = firebase.storage()
img_dir = "dataset"
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


def getImageAndLabels(img_dir):
    imagePaths = [os.path.join(img_dir, f) for f in os.listdir(img_dir)]
    faceSamples = []
    labels = []

    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')
        id_img = int(os.path.split(imagePath)[-1].split(".")[0])
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y+h, x:x+w])
            labels.append(id_img)
    return faceSamples, labels


@bp_training.route('/api/training')
def train_model():
    try:
        print("\nFace training. please wait...")
        faces, ids = getImageAndLabels(img_dir)
        recognizer.train(faces, np.array(ids))
        if os.path.isfile("models/model.yml") == True:
            os.remove("models/model.yml")
            recognizer.write("models/model.yml")
            print("\nTraining success !")
            # print("\n{0} faces are learned.".format(len(np.unique(ids))))
            storage.child('model.yml').put('models/model.yml')
            print('Uploaded the model')
            return jsonify({'success': True}), 200
        else:
            recognizer.write("models/model.yml")
            print("\nTraining success !")
            storage.child('model.yml').put('models/model.yml')
            print('Uploaded the model')
            # print("\n{0} faces are learned.".format(len(np.unique(ids))))
            return jsonify({'success': True}), 200
    except Exception as e:
        print(e)
