########################################################################
#ESP32 Cam Facial Recognition
#Copyleft Shravan Shankar C S 2024; see the INFO.md file for authorship.

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program in the LICENSE file.
#If it is not there, see <http://www.gnu.org/licenses/>.
########################################################################

import pandas as pd
import cv2
import urllib.request
import numpy as np
import os
from datetime import datetime
import face_recognition
import time

path = r'./Training_images'
url = 'http://192.168.178.117/cam-hi.jpg'
log_file = 'Log.csv'

if not os.path.exists(log_file):
    df = pd.DataFrame(columns=['Name', 'Time'])
    df.to_csv(log_file, index=False)

images = []
classNames = []

def load_images_from_directory():
    myList = os.listdir(path)
    newImages = []
    newClassNames = []
    encodedNames = [os.path.splitext(name)[0] for name in classNames]
    for cl in myList:
        name_parts = cl.replace("_", " ").split()
        formatted_name = "_".join(part.capitalize() for part in name_parts)
        file_name, file_extension = os.path.splitext(cl)
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        
        if file_extension.lower() not in valid_extensions:
            continue

        if file_extension == '':
            sanitized_name = f"{formatted_name}{file_extension.lower()}"
            if cl != sanitized_name and cl not in encodedNames:
                old_file_path = os.path.join(path, cl)
                new_file_path = os.path.join(path, sanitized_name)
                print(f"Renaming: {cl} -> {sanitized_name}")
                os.rename(old_file_path, new_file_path)
                cl = sanitized_name

        name = os.path.splitext(cl)[0]
        if name not in encodedNames:
            curImg = cv2.imread(f'{path}/{cl}')
            if curImg is not None:
                newImages.append(curImg)
                newClassNames.append(name)
    return newImages, newClassNames

def format_display_name(name):
    name = name.replace("_", " ")
    return " ".join(word.capitalize() for word in name.split())

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def logPerson(name):
    display_name = format_display_name(name)
    with open(log_file, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if display_name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{display_name},{dtString}')

newImages, newClassNames = load_images_from_directory()
images.extend(newImages)
classNames.extend(newClassNames)

encodeListKnown = findEncodings(images)
print('Encoding Complete')

last_scanned = time.time()

while True:
    if time.time() - last_scanned > 10:
        newImages, newClassNames = load_images_from_directory()
        if newImages:
            images.extend(newImages)
            classNames.extend(newClassNames)
            encodeListKnown.extend(findEncodings(newImages))
            print('New images encoded:', [format_display_name(name) for name in newClassNames])
        last_scanned = time.time()

    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgnp, -1)

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex]
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, format_display_name(name), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            logPerson(name)

    cv2.imshow('Webcam', img)
    key = cv2.waitKey(5)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
