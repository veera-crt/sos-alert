import cv2
import sounddevice as sd
import queue
import sys
import json
from vosk import Model, KaldiRecognizer

# Path to the Vosk model
MODEL_PATH = "/Users/veerapandig/Projects/alert sys/model"

# Load the Vosk Model
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# Queue to store audio data
q = queue.Queue()

# Callback function to capture audio
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# Function to turn on the camera
def activate_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("SOS Camera Active", frame)
        cv2.imwrite("sos_capture.jpg", frame)  # Save image

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Start Listening for Voice Command
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                        channels=1, callback=callback):
    print("Listening for 'help me'... Speak now!")

    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print("Detected:", result)

            text = json.loads(result).get("text", "")

            if "help me" in text:
                print("⚠️ SOS TRIGGERED! Activating Camera... ⚠️")
                
                # Directly call `activate_camera()` instead of using a thread
                activate_camera()
                break
