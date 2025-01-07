#!/usr/bin/env python3

import json
import sounddevice as sd
import numpy as np
import wave
import threading
import time
from datetime import datetime
from pynput import keyboard
import os

# Configuration
SAMPLERATE = 44100
CHANNELS = 1
SUBTYPE = 'PCM_16'  # Ensure proper audio format
DATA_DIR = "./data"

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Generate filenames based on timestamp
start_time = datetime.now()
AUDIO_FILENAME = os.path.join(DATA_DIR, start_time.strftime("%Y-%m-%d_%H-%M-%S.wav"))
KEYSTROKE_FILENAME = os.path.join(DATA_DIR, start_time.strftime("%Y-%m-%d_%H-%M-%S.json"))

# Shared flag to stop the threads
stop_flag = threading.Event()

def record_audio():
    """Record audio from the microphone."""
    print("Recording audio...")
    audio_data = []

    def callback(indata, frames, time, status):
        if status:
            print(f"Audio input error: {status}")
        audio_data.append(indata.copy())

    try:
        with sd.InputStream(samplerate=SAMPLERATE, channels=CHANNELS, dtype='int16', callback=callback):
            while not stop_flag.is_set():
                sd.sleep(100)
    except Exception as e:
        print(f"Audio recording error: {e}")
        stop_flag.set()
        return

    # Save audio to a file
    audio_data = np.concatenate(audio_data, axis=0)
    with wave.open(AUDIO_FILENAME, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(SAMPLERATE)
        wf.writeframes(audio_data.tobytes())

    print(f"Audio saved to {AUDIO_FILENAME}")



def log_keystrokes():
    """Log keystrokes to a file."""
    print("Logging keystrokes...")
    keystroke_log = []

    def on_press(key):
        t = time.time()
        keystroke_log.append({"direction": "down", "key": str(key), "timestamp": t})

        return True

    def on_release(key):
        t = time.time()
        keystroke_log.append({"direction": "up", "key": str(key), "timestamp": t})

        if key == keyboard.Key.enter:
            stop_flag.set()
            with open(KEYSTROKE_FILENAME, "w") as f:
                json.dump(keystroke_log, f, indent=4)
                print(f"Keystrokes logged to {KEYSTROKE_FILENAME}")
                stop_flag.set()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while not stop_flag.is_set():
            time.sleep(0.1)
        input()


if __name__ == "__main__":
    # Run audio recording and keystroke logging concurrently
    audio_thread = threading.Thread(target=record_audio)
    keystroke_thread = threading.Thread(target=log_keystrokes)

    audio_thread.start()
    keystroke_thread.start()

    audio_thread.join()
    keystroke_thread.join()

    print("Recording and logging complete.")
