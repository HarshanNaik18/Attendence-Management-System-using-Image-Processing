import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("FirebaseKeys.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
studentRef = db.collection("DBMS")

print("Fetching data from database")
docs = studentRef.stream()

print("\nDBMS Class Details : \n")
    # studentData[doc.id] = doc.to_dict()
for doc in docs:
    id = doc.id
    data = doc.to_dict()
    print("Class no : ",id)
    print("Present : ",data["Present"])
    print("Absent : ",data["Absent"])
    print("Total : ",data["Total"])
    print("Strength : ",data["Strength"])
    print("Time : ",data["Time"])
    print("Attendance :")
    for std in data["Attendence"].values():
        print("\t",std)
    print("\n")