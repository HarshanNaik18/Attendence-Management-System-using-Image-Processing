import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
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
firebase_admin.initialize_app(cred)

db = firestore.client()
studentRef = db.collection("DAA")

print("Fetching data from database")
docs = studentRef.stream()

print("\nDAA Class Details : \n")
# studentData[doc.id] = doc.to_dict()
for doc in docs:
    id = doc.id
    data = doc.to_dict()
    print("Class no : ", id)
    print("Present : ", data["Present"])
    print("Absent : ", data["Absent"])
    print("Total : ", data["Total"])
    print("Strength : ", data["Strength"])
    print("Time : ", data["Time"])
    print("Attendance :")
    for std in data["Attendence"].values():
        print("\t", std)
    print("\n")
