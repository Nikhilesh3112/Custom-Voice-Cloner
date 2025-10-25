import pyaudio
import wave
import speech_recognition as sr


import subprocess

# Define the audio parameters
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (samples per second)
CHUNK = 1024  # Size of each audio chunk
RECORD_SECONDS = 5  # Duration of recording in seconds

        
for ij in range(0,51):
    # Convert speech to text
    recognizer = sr.Recognizer()
    with sr.AudioFile('Me/'+str(ij)+'.wav') as source:
        audio_data = recognizer.record(source)
        try:
            text_rec = recognizer.recognize_google(audio_data)
            print(f"Recognized text: {text_rec}")
            
            # Write the recognized text to a Notepad file
            with open('tx1/'+str(ij)+'.txt', 'w') as notepad:
                notepad.write(text_rec)
            
            print(f"Recognized text saved in {'tx1/'+str(ij)+'.wav'}")
            
            # Open the Notepad file with the recognized text
            subprocess.Popen(['notepad.exe', 'tx1/'+str(ij)+'.wav'])        
            
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")