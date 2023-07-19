import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage


cred = credentials.Certificate("FirebaseKeys.json")
firebase_admin.initialize_app(cred,{
    'storageBucket': 'attendance-management-sys-01.appspot.com'
})

db = firestore.client()


studentRef = db.collection("students")
docs = studentRef.stream()
studentData = dict()

for doc in docs:
    studentData[doc.id] = doc.to_dict()


cam = cv2.VideoCapture(0)


print("Loading encode file")

file = open("EncodeFile.p", 'rb')
encodeListKnownIds = pickle.load(file)
file.close()


encodeListKnown, studentIds = encodeListKnownIds
print("Encode file Loaded")

counter = 0
id = -1

while True:
    success, img = cam.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame = face_recognition.face_encodings(imgs, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDist)
        if matches[matchIndex]:
            print(studentData[studentIds[matchIndex]])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox = x1, y1, x2-x1, y2-y1
            cvzone.cornerRect(img, bbox, rt=0)

    cv2.imshow("Attendance System", img)
    cv2.waitKey(1)
