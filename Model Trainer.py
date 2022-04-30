import cv2
import numpy as np
from PIL import Image
import os

path = 'Samples'   # Path for samples already taken

recognizer = cv2.face.LBPHFaceRecognizer_create()   # Local Binary Patterns Histograms
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def Images_And_Labels(path):  # Function to fetch the images and labels

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:  # To iterate particular image path
        
        gray_img = Image.open(imagePath).convert('L')  # Convert it to greyscale
        img_arr = np.array(gray_img,'uint8')  # Creating an array

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_arr)

        for (x,y,w,h) in faces:
            faceSamples.append(img_arr[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples, ids

print("Training faces. It will take a few seconds wait...")

faces,ids = Images_And_Labels(path)
recognizer.train(faces, np.array(ids))

recognizer.write('Trainer/Trainer.yml')  # Save trained model as trainer.yml

print("Model trained, Now we can recognize your face.")