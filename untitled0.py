import pyaudio
import wave
import speech_recognition as sr

import subprocess



try:
     
    
    # Define the audio parameters
    FORMAT = pyaudio.paInt16  # Audio format
    CHANNELS = 1  # Mono audio
    RATE = 44100  # Sample rate (samples per second)
    CHUNK = 1024  # Size of each audio chunk
    RECORD_SECONDS = 5  # Duration of recording in seconds
    
        
    # Convert speech to text
    recognizer = sr.Recognizer()
    with sr.AudioFile(str(100)+'.wav') as source:
        audio_data = recognizer.record(source)
        try:
            text_rec = recognizer.recognize_google(audio_data)
            print(f"Recognized text: {text_rec}")
            
            # Write the recognized text to a Notepad file
            with open(str(100)+'.txt', 'w') as notepad:
                notepad.write(text_rec)
            
            
            # Open the Notepad file with the recognized text
            subprocess.Popen(['notepad.exe', str(100)+'.txt'])        
            
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
    
    # # Define the audio parameters
    # FORMAT = pyaudio.paInt16  # Audio format
    # CHANNELS = 1  # Mono audio
    # RATE = 44100  # Sample rate (samples per second)
    # CHUNK = 1024  # Size of each audio chunk
    # RECORD_SECONDS = 5  # Duration of recording in seconds
    # OUTPUT_FILENAME = "output.wav"  # Name of the output .wav file
    
    # # Initialize the audio stream
    # audio = pyaudio.PyAudio()
    
    # # Create an audio stream
    # stream = audio.open(format=FORMAT, channels=CHANNELS,
    #                     rate=RATE, input=True,
    #                     frames_per_buffer=CHUNK)
    
    # print("Recording...")
    
    # frames = []
    
    # # Capture audio data
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #     data = stream.read(CHUNK)
    #     frames.append(data)
    
    # print("Finished recording.")
    
    # # Stop and close the audio stream
    # stream.stop_stream()
    # stream.close()
    # audio.terminate()
    
    # # Save the audio data to a .wav file
    # with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    #     wf.setnchannels(CHANNELS)
    #     wf.setsampwidth(audio.get_sample_size(FORMAT))
    #     wf.setframerate(RATE)
    #     wf.writeframes(b''.join(frames))
    
    # print(f"Audio saved as {OUTPUT_FILENAME}")
    
    # # Convert speech to text
    # recognizer = sr.Recognizer()
    # with sr.AudioFile(OUTPUT_FILENAME) as source:
    #     audio_data = recognizer.record(source)
    #     try:
    #         text_rec = recognizer.recognize_google(audio_data)
    #         print(f"Recognized text: {text_rec}")
            
    #         # Write the recognized text to a Notepad file
    #         with open('test text/1.txt', 'w') as notepad:
    #             notepad.write(text_rec)
            
    #         print(f"Recognized text saved in {'1.txt'}")
            
    #         # Open the Notepad file with the recognized text
    #         subprocess.Popen(['notepad.exe', "test text/1.txt"])        
            
    #     except sr.UnknownValueError:
    #         print("Could not understand the audio")
    #     except sr.RequestError as e:
    #         print(f"Could not request results; {e}")
    
    # You can now use the 'text' variable containing the recognized text as needed.
    
    import numpy as np
    
    
    import os
    import glob
    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.metrics import accuracy_score
    
    # Step 1: Define a function to read and preprocess text data from multiple files.
    def read_and_preprocess_data(file_paths):
        data = []
        labels = []
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Perform any necessary data preprocessing here, such as text cleaning.
                # You can use regular expressions or other techniques to clean the text.
                data.append(content)
                labels.append(os.path.basename(file_path).split('.')[0])  # Use the file name as a label.
        return data, labels
    
    # Step 2: Specify the directory containing your text files.
    data_dir = 'Text/'
    
    # Step 3: Use glob to find all text files in the directory.
    file_paths = glob.glob(os.path.join(data_dir, '*.txt'))
    
    # Step 4: Read and preprocess the data.
    data, labels = read_and_preprocess_data(file_paths)
    
    reviews = text_rec
    default_ans = data
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    cosine_sim = []
    for ii in range(0,len(data)):
        
        # Two strings to compare
        string1 = default_ans[ii]
        string2 = text_rec
        
        # Initialize the TF-IDF vectorizer
        vectorizer = TfidfVectorizer()
        
        # Transform the strings into TF-IDF vectors
        tfidf_matrix = vectorizer.fit_transform([string1, string2])
        
        # Calculate the cosine similarity between the vectors
        cosine_sim.append(cosine_similarity(tfidf_matrix[0], tfidf_matrix[1]))
        res = np.max(cosine_sim)
    print("Cosine Similarity:", cosine_sim)
    
    IDX = cosine_sim.index(res)
    
    
    from pydub import AudioSegment
    from pydub.playback import play
    import noisereduce as nr
    
    import streamlit as st
        
    
    
    from scipy.io import wavfile
    samplerate, data = wavfile.read('res.wav')
        
    from scipy.io import wavfile
    samplerate, data = wavfile.read('res.wav')
    
    file1 = open("Text/"+str(IDX)+".txt","r")
    Voice_ch = file1.read()


    # Load the audio file
    # samplerate1, data1 = wavfile.read("Me/"+str(IDX)+".wav")

    audio = AudioSegment.from_file("Me/"+str(IDX)+".wav", format="wav")
    # filtered_audio = audio.low_pass_filter(0.01)
    
    
    # Change the pitch
    octaves = 0.9  # You can adjust this value to change the pitch
    new_audio = audio.speedup(playback_speed=1.3 / octaves)
    
    
    # Play the modified audio
    play(new_audio)
    
    
    # Save the modified audio to a new file
    new_audio.export("Final_res.wav", format="wav")

except:
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(text_rec)
    engine.runAndWait()

