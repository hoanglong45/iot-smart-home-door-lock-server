import os
import glob
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

firebase = Firebase(config)
db = firebase.database()
storage = firebase.storage()

# print(show_token)

# new_file = open("test.txt", "w")
# new_file.write('Hello World')
# a = storage.child('test.txt').put('test.txt')
# print(a)


# all_users = db.child('Users').get()
# for user in all_users.each():
#     name = user.val()['name']
#     rfid = user.val()['rfid']
#     for i in range(0, 4):
#         storage.child(
#             f'Users/{name}-{rfid}/{rfid}.{i}').download(f'raw_dataset/{rfid}.{i}.jpg')


# import cv2
# import glob

# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# count = 0

# for filepath in glob.glob('raw_dataset/*.jpg'):
#     image = cv2.imread(filepath)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#     for (x, y, w, h) in faces:
#         cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
#         count += 1
#         roi_gray = gray[y:y+h, x:x+w]
#         cv2.imwrite(f"dataset/user.{str(count)}.jpg", roi_gray)
#         cv2.imshow("image", image)

# def get_user_by_rfid(rfid):
#     all_users = db.child('Users').get()
#     for user in all_users.each():
#         if rfid == user.val()['rfid']:
#             name = user.val()['name']
#             print('name', name)


# get_user_by_rfid('789456')

def iterate():
    img_dir = 'dataset'
    imagePaths = [os.path.join(f) for f in os.listdir(img_dir)]

    for filename in imagePaths:
        # print(filename[f'{int(rfid)}.1.jpg'])
        print(filename[0])


iterate()
