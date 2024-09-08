import numpy as np
from imgbeddings import imgbeddings
from PIL import Image
import cv2
import os
from fastapi import HTTPException

class FaceRecognition:
    def __init__(self, img_upload=None):
        path_dir = os.getcwd()
        alg = path_dir + "/services/" +"haarcascade_frontalface_default.xml"
        self.haar_cascade = cv2.CascadeClassifier(alg)
        img = Image.open(img_upload.file).convert("L")
        self.img = np.array(img)
        
    def normalize_vector(self, vector):
        return vector / np.linalg.norm(vector)
    
    def to_embeddings(self):
        if self.img is None:
            raise HTTPException(status_code=400, detail="Image not found")
        ibed = imgbeddings()
        faces = self.haar_cascade.detectMultiScale(
            self.img,
            scaleFactor=1.05,
            minNeighbors=2,
            minSize=(200, 200)
        )
        
        faces_detected = len(faces)
        if(faces_detected == 0):
            raise HTTPException(status_code=400, detail="No face detected")
        if(faces_detected > 1):
            raise HTTPException(status_code=400, detail="More than one face detected")
        
        for x, y, w, h in faces:
            cropped_image = self.img[y : y + h, x : x + w]
            pil_image = Image.fromarray(cropped_image).convert('RGB')
            embedding = ibed.to_embeddings(pil_image)[0]
            
        return self.normalize_vector(embedding)
    
