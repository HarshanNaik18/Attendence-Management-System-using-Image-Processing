import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import os

cred = credentials.Certificate("FirebaseKeys.json")
firebase_admin.initialize_app(cred,{
    'storageBucket': 'attendance-management-sys-01.appspot.com'
})

bucket = storage.bucket()

folderPath = 'images'
PathList = os.listdir(folderPath)
imgList = []
studentIds = []
for path in PathList:
    studentIds.append(os.path.splitext(path)[0])
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    blob.make_public()
    imgList.append(blob.public_url)

# print(imgList)

db = firestore.client()

data = {
    "21003": {
        "usn": '1BG21IS003',
        "Name": "Aishwarya N",
        "Branch": "ISE",
        "Sem": 4,
        "Attendance":{
            "MATHS":{
                "Attended":7,
                "Total":10,
                "Percentage":70
            },
            "MES":{
                "Attended":8,
                "Total":10,
                "Percentage":80
            },
            "DAA":{
                "Attended":6,
                "Total":10,
                "Percentage":60
            },
            "DBMS":{
                "Attended":10,
                "Total":10,
                "Percentage":100
            },
            "APA":{
                "Attended":7,
                "Total":7,
                "Percentage":100
            },
        },
        "Img":imgList[0]
    },
    "21005": {
        "usn": '1BG21IS005',
        "Name": "Akshay Cavale",
        "Branch": "ISE",
        "Sem": 4,
        "Attendance":{
            "MATHS":{
                "Attended":7,
                "Total":10,
                "Percentage":70
            },
            "MES":{
                "Attended":8,
                "Total":10,
                "Percentage":80
            },
            "DAA":{
                "Attended":6,
                "Total":10,
                "Percentage":60
            },
            "DBMS":{
                "Attended":10,
                "Total":10,
                "Percentage":100
            },
            "APA":{
                "Attended":7,
                "Total":7,
                "Percentage":100
            },
        },
        "Img":imgList[1]
    },
    "21027": {
        "usn": '1BG21IS027',
        "Name": "Harshan Naik",
        "Branch": "ISE",
        "Sem": 4,
        "Attendance":{
            "MATHS":{
                "Attended":7,
                "Total":10,
                "Percentage":70
            },
            "MES":{
                "Attended":8,
                "Total":10,
                "Percentage":80
            },
            "DAA":{
                "Attended":6,
                "Total":10,
                "Percentage":60
            },
            "DBMS":{
                "Attended":10,
                "Total":10,
                "Percentage":100
            },
            "APA":{
                "Attended":7,
                "Total":7,
                "Percentage":100
            },
        },
        "Img":imgList[2]
    }
}

for key, item in data.items():
    studentRef = db.collection("students").document(key)
    studentRef.set(item)
