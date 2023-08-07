import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("FirebaseKeys.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
studentRef = db.collection("students")

print("Fetching data from database")
docs = studentRef.stream()

print("Students Details : \n")
    # studentData[doc.id] = doc.to_dict()
for doc in docs:
    id = doc.id
    data = doc.to_dict()
    print("USN : ",id)
    print("Name : ",data["Name"])
    print("Branch : ",data["Branch"])
    print("Sem : ",data["Sem"])
    print("Attendance : ")
    print("\tAPA : ",data["Attendance"]["APA"])
    print("\tDAA : ",data["Attendance"]["DAA"])
    print("\tDBMS : ",data["Attendance"]["DBMS"])
    print("\tMATHS : ",data["Attendance"]["MATHS"])
    print("\tMES : ",data["Attendance"]["MES"])
    print("\n")
