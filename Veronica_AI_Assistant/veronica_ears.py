import os
import requests
from faster_whisper import WhisperModel
import sounddevice as sd
from kokoro import KPipeline
import numpy as np
import time

# Hide warnings for a clean look
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import warnings
warnings.filterwarnings("ignore")

# CONFIGURATION 
MIC_ID = None  # Your working microphone number
WEBHOOK_URL = "http://localhost:5678/webhook/veronica-voice"


print("Initializing Veronica...")
model = WhisperModel("small.en", device="cpu", compute_type="int8")
voice_pipeline = KPipeline(lang_code='a')

def speak(text):
    cleaned_text = text.replace("**", "").replace("*", "").replace("#", "").strip()
    print(f"Veronica: {text}")
    generator = voice_pipeline(text, voice='af_bella', speed=1.1) 
    for gs, ps, audio in generator:
        sd.play(audio, 24000)
        sd.wait()
    time.sleep(0.5)  # Making the speakers completely go silent before mic opens

def listen(seconds):
    fs = 16000
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, device=MIC_ID)
    sd.wait()
    return recording.flatten().astype(np.float32)

def main():
    print("System Active")
    print("\n[STANDBY] Listening for wake word...")
    
    while True:
        audio_data = listen(4)
        
        segments, _ = model.transcribe(audio_data)
        wake_text = " ".join([s.text for s in segments]).strip().lower()

        
        # If it hears literally anything, print it out so we can see it.
        if wake_text:
            print(f"[Debug] Standby heard: '{wake_text}'")

        if "veronica" in wake_text:
            speak("Yes, Boss?")
            
            while True:
                print("\n>>> [AWAKE] Listening for your command...")
                command_audio = listen(6) 
                segments, _ = model.transcribe(command_audio)
                command_text = " ".join([s.text for s in segments]).strip()
                
                print(f"--- Captured Command: '{command_text}' ---")
                
                # Check for silence IMMEDIATELY
                if not command_text or not command_text.strip():
                    print("Silence detected. Staying awake...")
                    continue
                
                if "go to sleep" in command_text.lower() or "goodbye" in command_text.lower():
                    speak("Goodbye Boss. Going back to standby mode.")
                    
                   
                    print("\n[STANDBY] Listening for wake word...")
                    
                    break 
                
                try:
                    response = requests.post(WEBHOOK_URL, json={"message": command_text})
                    res_data = response.json()
                    
                    if isinstance(res_data, list) and len(res_data) > 0:
                        reply = res_data[0].get('output', "Task complete.")
                    elif isinstance(res_data, dict):
                        reply = res_data.get('output', "Task complete.")
                    else:
                        reply = "Task complete."
                        
                    speak(reply)
                    
                except Exception as e:
                    print(f"Connection error: {e}")
                    speak("I am having trouble connecting to my core network.")
                    break

if __name__ == "__main__":
    main()