import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("FirebaseKeys.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

data = {
    "21003": {
        "usn": '1BG21IS003',
        "Name": "Aishwarya N",
        "Branch": "ISE",
        "Sem": 4,
        "Attendance_Count": 15
    },
    "21005": {
        "usn": '1BG21IS005',
        "Name": "Akshay Cavale",
        "Branch": "ISE",
        "Sem": 4,
        "Attendance_Count": 10
    },
    "21027": {
        "usn": '1BG21IS027',
        "Name": "Harshan Naik",
        "Branch": "ISE",
        "Sem": 4,
        "Attendance_Count": 20
    }
}

for key, item in data.items():
    studentRef = db.collection("students").document(key)
    studentRef.set(item)
