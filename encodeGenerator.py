import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


cred = credentials.Certificate("FirebaseKeys.json")
firebase_admin.initialize_app(cred,{
    'storageBucket': 'attendance-management-sys-01.appspot.com'
})

bucket = storage.bucket()

folderPath = 'images'
PathList = os.listdir(folderPath)
# print(PathList)


imgList = []
studentIds = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList



print("Encoding started")
encodeListKnown = findEncodings(imgList)
encodeListKnownIds = [encodeListKnown, studentIds]
print("Encoding completed")

file = open("EncodeFile.p", "wb")
pickle.dump(encodeListKnownIds, file)
file.close()
print("File saved")
