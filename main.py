import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import urllib.request

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

connection = connect()
counter = 0
while not connection:
    if counter%20000 == 0:
        print("Please connect internet")
    connection = connect()
    counter = counter + 1

print( "connected")

cred = credentials.Certificate("FirebaseKeys.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
studentRef = db.collection("students")

print("Fetching data from database")
docs = studentRef.stream()

studentData = dict()

for doc in docs:
    studentData[doc.id] = doc.to_dict()

print("Fetched data from databse\n")

# Class details
AllCourses = ["MATHS","MES","DAA","DBMS","APA"]

course = AllCourses[1]
class_starting_time = datetime(2023, 7, 25, 10, 0)
class_ending_time = datetime(2023, 8, 7, 23, 00, 40)

attendance = dict()

for key, value in studentData.items():
    info = {
        "Name": value["Name"],
        "usn": value["usn"],
        "Status" : "Absent"
    }
    attendance[key]=info


print("Loading encode file")

file = open("EncodeFile.p", 'rb')
encodeListKnownIds = pickle.load(file)
file.close()

encodeListKnown, studentIds = encodeListKnownIds
print("Encode file Loaded\n")


flag = False
cam = cv2.VideoCapture(0)

while True:
    cur_time = datetime.now()

    if cur_time >= class_starting_time and cur_time < class_ending_time :
        flag = True
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
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = x1, y1, x2-x1, y2-y1
                cvzone.cornerRect(img, bbox, rt=0)
                if attendance[studentIds[matchIndex]]["Status"] == "Absent":
                    print(studentData[studentIds[matchIndex]])
                    attendance[studentIds[matchIndex]]["Status"] = "Present"
                else :
                    print(studentData[studentIds[matchIndex]]["Name"] ," your Attendance is already marked\n")
                
        cv2.imshow("Attendance System", img)
        cv2.waitKey(1)

    else:
        break

if(flag):
    present_count = 0
    absent_count = 0
    class_count = 0
    print("Updating database")
    for key, value in attendance.items():
        
        if value["Status"] == "Present":
            present_count += 1

            Attended = studentData[key]["Attendance"][course]["Attended"] + 1
            Total = studentData[key]["Attendance"][course]["Total"] + 1
            Percentage = (Attended/Total)*100
            class_count = Total

            studentData[key]["Attendance"][course]["Attended"] = Attended
            studentData[key]["Attendance"][course]["Total"] = Total
            studentData[key]["Attendance"][course]["Percentage"] = Percentage

            studentRef.document(key).update({"Attendance":studentData[key]["Attendance"]})

        else:
            absent_count += 1

            Attended = studentData[key]["Attendance"][course]["Attended"]
            Total = studentData[key]["Attendance"][course]["Total"] + 1
            Percentage = (Attended/Total)*100
            class_count = Total

            studentData[key]["Attendance"][course]["Attended"] = Attended
            studentData[key]["Attendance"][course]["Total"] = Total
            studentData[key]["Attendance"][course]["Percentage"] = Percentage

            studentRef.document(key).update({"Attendance":studentData[key]["Attendance"]})

    attendance_Sheet = {
        "Time": datetime.utcnow(),
        "Attendence":attendance,
        "Present":present_count,
        "Absent":absent_count,
        "Strength":(present_count/len(attendance))*100,
        "Total":len(attendance)
    }

    docName = course+f'{class_count}'

    courseRef = db.collection(course).document(docName)
    courseRef.set(attendance_Sheet)

    print("Databse Updated")

else:
    print("No class scheduled")