# For CNN
import serial
import time
import schedule
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
from keras.models import model_from_json
import cv2
import numpy as np

# For ECG
import h5py
import pandas as pd
import numpy as np
import wfdb
import pickle
from ecgdetectors import Detectors

#Main Output
output = 0

#CNN Code

list_values = []
list_in_floats = []

print('Program started')

model = model_from_json(open("C:\\Users\\arkap\\Desktop\\Project\\model.json", "r").read())
model.load_weights('C:\\Users\\arkap\\Desktop\\Project\\model.h5')
face_classifier = cv2.CascadeClassifier('C:\\Users\\arkap\\Desktop\\Project\\haarcascade_frontalface_default.xml')

#emotion_labels = ['negative','neutral', 'positive']
emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral','Sad','Surprise']

cap = cv2.VideoCapture(0)

mood=[]

while True:
    _, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    faces = face_classifier.detectMultiScale(gray,minNeighbors=5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)



        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)

            prediction = model.predict(roi)#[0]
            label=emotion_labels[prediction.argmax()]
            mood.append(label)
            label_position = (x,y)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        else:
            cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow('Emotion Detector',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
 
for i in range(0,20):
    if mood[i] == 'Neutral' or mood[i] == 'Disgust':
        output = output + 0
    elif mood[i] == 'Sad' or mood[i] == 'Angry' or mood[i] == 'Fear' or mood[i] == 'Surprised':
        output = output - 0.5
    elif mood[i] == 'Happy':
        output = output + 0.5
print(output)
print(mood)

#ECG Code

# Function for RR Distance
def rr_distance(signals):
    detectors = Detectors(360)
    r_peaks = detectors.pan_tompkins_detector(signals)
    peaks = np.array(r_peaks)
    avg = []
    for i in range(0,len(r_peaks)-1):

        dist = peaks[i]-peaks[i+1]
        avg.append(dist)
    return (-np.average(avg)),r_peaks

# Function for Denoising
def denoising(y, threshold, sample_rate):
    n = len(y)
    fhat = np.fft.fft(y, n) #computes the fft
    psd = fhat * np.conj(fhat)/n
    freq = (1/(sample_rate*n)) * np.arange(n) #frequency array
    idxs_half = np.arange(1, np.floor(n/2), dtype=np.int32)
    psd_idxs = psd > threshold #array of 0 and 1
    psd_clean = psd * psd_idxs #zero out all the unnecessary powers
    fhat_clean = psd_idxs * fhat #used to retrieve the signal

    signal_filtered = np.fft.ifft(fhat_clean) #inverse fourier transform
    
    return signal_filtered

data = pd.read_csv('C:\\Users\\arkap\\Desktop\\Project\\data.csv')
arr = data.to_numpy()
signal = (arr.transpose())
#signal_filtered = denoising(signal,30,1000)
RR,r_peaks = rr_distance(signal)
RR = RR/100
Amplitude = ((np.max(signal))/10000)            

Medicine_Yes = input("Enter 1 if under medication: ")
Age = input("Enter age/100: ")
Sex_M = input("Enter 1 if male and vice versa: ")

#df = pd.DataFrame({'Amplitude':[0.915824],'RR':[1.841667],'Age':[Age],'Sex_M':[Sex_M],'Medicine_Yes':[Medicine_Yes]})
df = pd.DataFrame({'Amplitude':[Amplitude],'RR':[RR],'Age':[Age],'Sex_M':[Sex_M],'Medicine_Yes':[Medicine_Yes]})

X = df

model = pickle.load(open('C:\\Users\\arkap\\Desktop\\Project\\pipe.pkl','rb'))  
predictions = model.predict(X)
# print(predictions)
if predictions == 1:
    output = output + 5
elif predictions == 2:
    output = output - 5 
else:
    output = output - 1
print(output) 


if 5<output<20:
    print('No Stress!')
elif -20<output<-5:
    print('High Stress!')
elif -5<output<5:
    print('Mild Stress!') 



