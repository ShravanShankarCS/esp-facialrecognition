# ESP32-CAM Facial-recognition

This is a fork of the open source code by @HowtoElectronics on YouTube. My goal is to not make massive changes, rather to just improve the detection system, styling, and fix some bugs. Please feel free to contribute if you want to make similar contributions,
or fork it if you'd like to make more sweeping changes.


## Who's behind this?

* HowtoElectronics - main.py v0.0.1 original author.
* Shravan Shankar C S - revamped, tweaked and fixed the code multiple times

## My contributions (Shravan Shankar C S)

<details>

<summary>Click to view</summary>

1. **Path Sanitization and Handling Spaces in Filenames**  
   Refactored the handling of filenames in the directory to manage spaces and replace them with underscores. Implemented a system to rename files containing spaces, ensuring filenames are sanitized before processing.

2. **Log File Handling**  
   Changed the log file's name from **"Attendance.csv"** to **"Log.csv"** to better reflect its role in logging entries. Ensured the log file is created if it doesn't exist and that new entries with a timestamp are appended when a face is recognized.

3. **Encoding Management**  
   Added a mechanism to check whether names have already been encoded, preventing redundant processing. This ensures previously encoded faces are not re-encoded, improving efficiency.

4. **Face Detection and Encoding**  
   Ensured the face recognition process only processes images that haven't been encoded yet. This prevents unnecessary re-encoding and ensures that new images are processed dynamically.

5. **Dynamic Directory Scanning**  
   Implemented a feature to scan the directory for new images every 10 seconds. This allows the program to update the list of known faces without needing a restart, enhancing adaptability.

6. **Improved Name Formatting**  
   Created a function to format the recognized names by capitalizing each word and replacing underscores with spaces. This improves the readability and user-friendliness of displayed names.

7. **Presence/Log Entry**  
   Replaced the **"markAttendance"** function with **"logPerson"**, updating the code to log entries in the **log file** whenever a recognized face is detected, along with the time of recognition.

8. **File Renaming on First Run**  
   Ensured files without a proper extension or those containing spaces are renamed to a more readable and consistent format on the first run of the program.

9. **Error Handling for Unsupported Image Formats**  
   Added error handling to skip unsupported image formats, such as non-image files or corrupted images, preventing the program from crashing.

10. **Code Refactoring and Optimization**  
    Refactored the code for better readability and efficiency, removing redundant checks, variables, and improving the overall modularity of functions.

</details>

## What's new?

* Version 0.4.4
* Made Python code a little bit more readable

