"""some detection here"""
import cv2
import numpy as np
import pickle

face_recognizer = cv2.face.LBPHFaceRecognizer_create()

face_cascade = cv2.CascadeClassifier('C:/Users/user/PycharmProjects/group_assignment/classifiers/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('C:/Users/user/PycharmProjects/group_assignment/classifiers/haarcascade_eye.xml')

face_recognizer.read('C:/Users/user/PycharmProjects/group_assignment/recognizer/training.yml')

labels = {}
with open('labels.pickle','rb') as f:
    og_labels = pickle.load(f)
    #reverse the elements in the dictionary
    labels = {v:k for k,v in og_labels.items()}
cam = cv2.VideoCapture(0)

while True:

    let,img = cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        #detect the eye still
        roi_gray = gray[y:int((y+h)*0.7),x:x+w]
        roi_color = img[y:y+h,x:x+w]
        id_,conf = face_recognizer.predict(roi_gray)#predict the region of interest
        if conf > 37:
            name = labels[id_]
            cv2.putText(img,name,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('faces detcted',img)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

