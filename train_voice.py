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


for ii in range(0,1):
    

    
    OUTPUT_FILENAME = "Me2/"+str(ii)+".wav"  # Name of the output .wav file
    
    # Initialize the audio stream
    audio = pyaudio.PyAudio()
    
    # Create an audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    
    print("Recording...")
    
    frames = []
    
    # Capture audio data
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Finished recording.")
    
    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Save the audio data to a .wav file
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    
    print(f"Audio saved as {OUTPUT_FILENAME}")
    
        
for ij in range(0,1):
    # Convert speech to text
    recognizer = sr.Recognizer()
    with sr.AudioFile('Me2/'+str(ij)+'.wav') as source:
        audio_data = recognizer.record(source)
        try:
            text_rec = recognizer.recognize_google(audio_data)
            print(f"Recognized text: {text_rec}")
            
            # Write the recognized text to a Notepad file
            with open('test text/'+str(ij)+'.txt', 'w') as notepad:
                notepad.write(text_rec)
            
            print(f"Recognized text saved in {'Me2/'+str(ij)+'.wav'}")
            
            # Open the Notepad file with the recognized text
            subprocess.Popen(['notepad.exe', 'Me2/'+str(ij)+'.wav'])        
            
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")