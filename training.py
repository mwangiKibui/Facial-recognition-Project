import os
import PIL
import cv2
import numpy as np
from PIL import Image
import pickle
face_cascade = cv2.CascadeClassifier('C:/Users/user/PycharmProjects/group_assignment/classifiers/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
base_dir = os.path.dirname(os.path.abspath(__file__))#getting the basedir
img_path = os.path.join(base_dir,'images')
#walk through the elements
current_id = 0
label_ids = {}
y_train = []
x_train = []
for path,dir,files in os.walk(img_path):
    #dir shall contain only the folders
    for file in files:
        if file.endswith(".jpg"):
            file_path = os.path.join(path,file)
            label = os.path.basename(path).replace(" ","-").lower()
            #send labels interms of a number,send the images as an numpy array and
            #convert the images to gray
            #converting the images to an array
            if current_id not in label_ids:
                label_ids[label] = current_id
            current_id += 1
            id_ = label_ids[label]
            pil_image = Image.open(file_path).convert("L")#shall convert it into a gray
            #resizing the image could mean match
            size = (500,500)
            final_image = pil_image.resize(size,Image.ANTIALIAS)
            image_array = np.array(final_image,"uint8")#uint8 as the type
            print(image_array)
            faces = face_cascade.detectMultiScale(image_array,1.5,5)
            for (x,y,w,h) in faces:
                roi = image_array[y:y+h,x:x+w]
                x_train.append(roi)
                y_train.append(id_)
with open("labels.pickle","wb") as f:
    pickle.dump(label_ids,f)
recognizer.train(x_train,np.array(y_train))
recognizer.save("recognizer/training.yml")

