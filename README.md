# ESP-Cam Facial Recognition

A project that uses OpenCV and ESP32's libraries to detect faces.

## Video Showcase

[![Project Showcase](https://i.imgur.com/su9OqSh.png)](https://youtu.be/LFXQLPcbmzs?feature=shared)

## Facial Recognition System Features


#### 1. **Facial Recognition for Attendance**:
   - Detects and recognizes faces in real-time using a webcam or camera feed.
   - Matches faces from the live feed with pre-encoded images in the system.
   - Marks attendance for recognized individuals by logging their names and time in a CSV file (`Log.csv`).
   - Ensures that names are formatted consistently, with spaces replaced by underscores and each word capitalized.

#### 2. **Dynamic Image Encoding**:
   - Continuously scans a specified directory for new images to encode, enabling "on-the-go" learning.
   - Automatically encodes new images as they are added to the directory without restarting the program.
   - Supports a variety of image file extensions (e.g., `.jpg`, `.jpeg`, `.png`, `.bmp`).

#### 3. **File Naming and Organization**:
   - Automatically renames images in the directory by replacing spaces with underscores and ensuring proper capitalization of each word.
   - Avoids renaming files that already have valid extensions, preventing errors from multiple extensions being added.

#### 4. **Real-Time Image Feed Processing**:
   - Continuously receives and processes frames from a camera feed (via URL or local webcam).
   - Resizes and processes frames efficiently for faster face recognition using face encodings.

#### 5. **Face Detection and Localization**:
   - Detects multiple faces in each frame with precise localization using the `face_recognition` library.
   - Draws bounding boxes around detected faces on the video feed.

#### 6. **Face Encoding and Matching**:
   - Encodes faces from training images and compares them against faces detected in real-time.
   - Uses facial encodings to match faces with the most accurate results using the `compare_faces` method.

#### 7. **Marking Log in CSV File**:
   - When a recognized face is detected, the system logs the individual’s name and the time they were detected in a CSV file.
   - Prevents duplicate entries by checking if the person has already been marked present.
   - Provides a time-stamped attendance record for each detected face.

#### 8. **Real-Time Feedback**:
   - Displays the real-time camera feed with bounding boxes around faces.
   - Shows the name of the recognized individual above their face, formatted with proper capitalization and space replacement.

#### 9. **Automatic File Naming and Sorting**:
   - Automatically updates image names in the directory by replacing spaces with underscores and capitalizing each word, ensuring consistent and readable filenames.

#### 10. **Automatic and Manual Face Recognition Updates**:
   - Automatically adds new images and names to the recognition system by periodically scanning the directory for changes.
   - Supports continuous learning by enabling the system to add new individuals without needing a restart.

#### 11. **Logging and Debugging**:
   - Provides logs in the terminal for images that are newly encoded and added to the system.
   - Offers useful print statements showing renamed files, encoded faces, and more for easier debugging and understanding of the system's flow.

#### 12. **Scalability**:
   - Can be easily scaled to accommodate additional images by simply adding them to the designated directory.
   - Supports growing databases of faces for larger applications (e.g., class attendance, office entry, etc.).

#### 13. **Cross-Platform Compatibility**:
   - The solution works on Windows, Linux, and macOS systems, provided all required dependencies are installed.

#### 14. **User-friendly Name Formatting**:
   - The system formats names for display, ensuring proper capitalization and avoiding file extension issues.
   - Converts the file names to a format that's readable and user-friendly, making it easier to understand who is detected.

#### 15. **Time Efficiency**:
   - The program scans the images directory every 10 seconds for new faces, ensuring it stays up-to-date with minimal processing delay.
   - Uses a smaller image resolution (downscaled by 4x) for faster face detection and encoding, ensuring performance stays high.

---

## To-Do list:  

#### 1. **Multi-Camera Support**:
   - Integrate support for multiple cameras or streams to enable real-time recognition from different sources simultaneously.

#### 2. **Mobile Integration**:
   - Develop a mobile app interface to interact with the system, display attendance logs, or provide real-time facial recognition results.

#### 3. **Enhanced Matching Algorithms**:
   - Implement additional algorithms or tweak the existing `face_recognition` library settings for better matching accuracy, especially in low-light or crowded environments.

#### 4. **Security Features**:
   - Add security layers, such as encrypted attendance logs or real-time alerts when unauthorized faces are detected.

#### 5. **User Interface (UI)**:
   - Develop a GUI for the system to make it more accessible for non-technical users to configure settings, view logs, and manage the database.

## Installation Steps

Follow these steps to get started with the project:

## 1. Clone the Repository

```bash
git clone https://github.com/ShravanShankarCS/esp-facialrecognition
cd esp-facialrecognition
```

## 2. Install CMake and Dlib

To set up the necessary environment:

1. Install Visual Studio Installer.
2. Add the "C++ Desktop Development Environment" using the VS Installer.
3. Ensure you select all **recommended packages** and make sure CMake is selected and remove IntelliCode (if you dont want 5GiB of AI you won't use. it extends installation time) before installation


## 3. Install Python Dependencies

- Please notethat it is very important that you do the second step before installing the python requirements.

Install the required Python dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## 4. Set Up Arduino IDE

1. Download and install the [Arduino IDE](https://www.arduino.cc/en/software).
2. Download the [Custom ESP-32 Camera Library](https://github.com/yoursunny/esp32cam)
3. Add the **ZIP library** to the Arduino IDE:
   - Go to `Sketch > Include Library > Add .ZIP Library`.
   - Select the necessary ZIP file.
   
   
## 5. Flashing the code into the ESP-Cam

1. Open the ESP-Cam.ino file
2. Make sure to enter in your WiFi Credentials in the code before flashing.
3. Make sure that in `Tools > Board`, you have the ESP32 Wrover Module selected. (It comes with the custom library linked above.).
4. Flash the code into the ESP-Cam.
5. Once finished, click the RST Button (Reset) and go to the Serial Monitor. If everything was done right in the ESP-32 Part, it will project the following:
```bash
CAMERA OK
http://127.0.0.1

  /cam-lo.jpg
  /cam-hi.jpg
  /cam-mid.jpg
```
- If it fails, it will print the following:
```bash
CAMERA FAIL
```

## 5. Configuring the Python script.

1. Open the main.py file.
2. In the `url` section, change the IP to the one you se on the Serial Monitor.
3. Execute the script.


## 6. Usage.

1. In the `Training-images` directory, add your images there. Make sure to add underscores `_` in the filename to seperate the name and surname. (If not, the python program will automatically do that.)
2. Execute the python script.
```bash
python3 main.py
```
3. Enjoy. :)

## Additional Notes

- Ensure your system has the latest Python version installed.
- Verify that your environment paths are set up correctly for CMake and Dlib.

## License

This project is licensed upon the [GNU License](https://www.gnu.org/).

## Contribution

Feel free to open issues or submit pull requests. Contributions are always welcome!
