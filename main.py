import pandas as pd
import cv2
import urllib.request
import numpy as np
import os
from datetime import datetime
import face_recognition
import time

# Path to images directory
path = r'./Training_images'

# URL for camera feed
url = 'http://192.168.178.117/cam-hi.jpg'

# Log file
log_file = 'Log.csv'

# Create log file if not exists
if not os.path.exists(log_file):
    df = pd.DataFrame(columns=['Name', 'Time'])
    df.to_csv(log_file, index=False)

# Initialize lists for images and names
images = []
classNames = []

# Function to load and encode images from directory
def load_images_from_directory():
    myList = os.listdir(path)
    newImages = []
    newClassNames = []
    encodedNames = [os.path.splitext(name)[0] for name in classNames]  # List of already encoded names
    for cl in myList:
        # Get the file extension and sanitize the name
        name_parts = cl.replace("_", " ").split()  # Split by space or underscore
        formatted_name = "_".join(part.capitalize() for part in name_parts)  # Join with underscore

        # Get the file extension (handle all extensions)
        file_name, file_extension = os.path.splitext(cl)
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        
        if file_extension.lower() not in valid_extensions:
            continue  # Skip files that don't have valid image extensions

        # Only rename if there is no file extension (just spaces need replacing)
        if file_extension == '':
            # Rename the file by replacing spaces with underscores
            sanitized_name = f"{formatted_name}{file_extension.lower()}"

            # Rename the file if necessary (Only once)
            if cl != sanitized_name and cl not in encodedNames:  # Rename only if different and not encoded
                old_file_path = os.path.join(path, cl)
                new_file_path = os.path.join(path, sanitized_name)
                print(f"Renaming: {cl} -> {sanitized_name}")
                os.rename(old_file_path, new_file_path)  # Rename the file
                cl = sanitized_name  # Update the filename to the sanitized version

        name = os.path.splitext(cl)[0]  # Remove file extension
        if name not in encodedNames:  # Only process new images
            curImg = cv2.imread(f'{path}/{cl}')
            if curImg is not None:
                newImages.append(curImg)
                newClassNames.append(name)
    return newImages, newClassNames

# Function to format names for display
def format_display_name(name):
    name = name.replace("_", " ")  # Replace underscores with spaces
    return " ".join(word.capitalize() for word in name.split())  # Capitalize each word

# Function to encode images
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Function to log people
def logPerson(name):
    display_name = format_display_name(name)  # Format name for display
    with open(log_file, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if display_name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{display_name},{dtString}')

# Load initial images and rename files
newImages, newClassNames = load_images_from_directory()
images.extend(newImages)
classNames.extend(newClassNames)

encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Camera feed loop
last_scanned = time.time()  # Track when directory was last scanned

while True:
    # Scan the directory every 10 seconds for new images
    if time.time() - last_scanned > 10:
        newImages, newClassNames = load_images_from_directory()
        if newImages:
            images.extend(newImages)
            classNames.extend(newClassNames)
            encodeListKnown.extend(findEncodings(newImages))
            print('New images encoded:', [format_display_name(name) for name in newClassNames])
        last_scanned = time.time()  # Update last scanned time

    # Read frame from camera
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgnp, -1)

    # Resize and convert for processing
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect and encode faces in the current frame
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

    # Display the video feed
    cv2.imshow('Webcam', img)
    key = cv2.waitKey(5)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
