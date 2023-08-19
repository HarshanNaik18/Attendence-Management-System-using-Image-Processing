import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import os
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
    if counter % 20000 == 0:
        print("Please connect internet")
    connection = connect()
    counter = counter + 1

print("connected")

cred = credentials.Certificate("FirebaseKeys.json")
firebase_admin.initialize_app(cred, {
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
    "1BG21IS003": {
        "usn": '1BG21IS003',
        "Name": "Aishwarya N",
        "Branch": "ISE",
        "Sem": 4,
        "Attendance": {
            "MATHS": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 0
            },
            "MES": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 0
            },
            "DAA": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 0
            },
            "DBMS": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 0
            },
            "APA": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 0
            },
        },
        "Img": imgList[0]
    },
    "1BG21IS005": {
        "usn": '1BG21IS005',
        "Name": "Akshay Cavale",
        "Branch": "ISE",
        "Sem": 4,
        "Attendance": {
            "MATHS": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 0
            },
            "MES": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 0
            },
            "DAA": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 0
            },
            "DBMS": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 0
            },
            "APA": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 0
            },
        },
        "Img": imgList[1]
    },
    "1BG21IS027": {
        "usn": '1BG21IS027',
        "Name": "Harshan Naik",
        "Branch": "ISE",
        "Sem": 4,
        "Attendance": {
            "MATHS": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 0
            },
            "MES": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 00
            },
            "DAA": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 0
            },
            "DBMS": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 0
            },
            "APA": {
                "Attended": 0,
                "Total": 0,
                "Percentage": 0
            },
        },
        "Img": imgList[2]
    }
}

print("Uploading student data to database")

for key, item in data.items():
    studentRef = db.collection("students").document(key)
    studentRef.set(item)

print("Uploaded to database")
