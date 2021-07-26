# Smart Home Door Lock - Server side

## Table of content
1. Introduction
2. Installation
3. Running the application

## Introduction
This is the source code for the Capstone Project

### Server folder
- `dataset`: Store the dataset of users.
- `models`: Store the model after training.
- `src/capture.py`: The file for the capture API.
- `src/training.py`: The file for the training API.
- `src/recognition`: The main file for recognition API for validation testing.
- `server.py`: The main file to start the server.

## Installation
- Install Anaconda from the official website - [Link](https://www.example.com)
- Open cmd in Windows and enter `conda activate`
- Install OpenCV: `pip install opencv-contrib-python`
- Install Flask: `pip install Flask`
- Install Firebase python libraray: `pip install firebase`
- Install some packages for Firebase: `pip install requests sseclient oauth2client gcloud requests_toolbelt python_jwt pycryptodome`

Note: Remember add configuration in `config`
```Python
config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": ""
}
```

# Running the application
Running the server-side
```sh
conda activate
cd server
python server.py
```
