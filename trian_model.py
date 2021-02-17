import cv2
import numpy as np
from os import listdir
import os
from os.path import isfile, join
from PIL import Image, ImageTk

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
data_path = './faces/user/'
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
Training_Data, Labels = [], []

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')

        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = face_classifier.detectMultiScale(imageNp)
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids

def testing():
    faces, Id = getImagesAndLabels("./faces/user/")
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(faces), np.asarray(Id))
    model.save("model/trained_model2.yml")
    print("Model trained sucessefully")