import pyaudio
import wave
import speech_recognition as sr
import streamlit as st
import subprocess

# App Title and Description
st.set_page_config(page_title="Custom Voice Cloner", page_icon="🎙️")
st.title("🎙️ Custom Voice Cloner")
st.markdown("""
### Welcome to Custom Voice Cloner!
This application allows you to speak a sentence and hear it played back in a different person's voice.

**How it works:**
1. Select a person whose voice you want to use
2. The app will record your voice for 5 seconds
3. Your speech is converted to text
4. Each word is matched with pre-recorded audio samples
5. The sentence is played back in the selected person's voice

---
""")

option = st.selectbox(
    '🎭 Select Person Voice',
    ('Select here...','Person1', 'Person2', 'Person3','Person4'))

if option != 'Select here...':
    st.info(f'You selected: **{option}**')
# agree = st.checkbox('Give Test Voice')

if option == 'Person1':
    try:
        
        st.success(' Ready to record! Speak clearly when recording starts.')
    
        
        # Define the audio parameters
        FORMAT = pyaudio.paInt16  # Audio format
        CHANNELS = 1  # Mono audio
        RATE = 44100  # Sample rate (samples per second)
        CHUNK = 1024  # Size of each audio chunk
        RECORD_SECONDS = 5  # Duration of recording in seconds
        OUTPUT_FILENAME = "output.wav"  # Name of the output .wav file
        
        # Initialize the audio stream
        audio = pyaudio.PyAudio()
        
        # Create an audio stream
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        
        print("Recording...")
        st.text("Recording...")
        
        frames = []
        
        # Capture audio data
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        print("Finished recording.")
        st.text("Finished recording....")
        
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
        st.write(f"Audio saved as {OUTPUT_FILENAME}")
        
        # Convert speech to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(OUTPUT_FILENAME) as source:
            audio_data = recognizer.record(source)
            try:
                text_rec = recognizer.recognize_google(audio_data)
                print(f"Recognized text: {text_rec}")
                st.write(f"Recognized text: {text_rec}")
                
                # Write the recognized text to a Notepad file
                with open('test text/1.txt', 'w') as notepad:
                    notepad.write(text_rec)
                
                print(f"Recognized text saved in {'1.txt'}")
                st.write(f"Recognized text saved in {'1.txt'}")
                
                
            except sr.UnknownValueError:
                print("Could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
        
        # You can now use the 'text' variable containing the recognized text as needed.
        
        import numpy as np
        
        # =======================
        import glob# Step 2: Specify the directory containing your text files.
        
        import numpy as np

                        
        
        import os
        import glob
        from sklearn.model_selection import train_test_split
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.metrics import accuracy_score
        
        data_dir = 'Text/'
        IDX = []
        # Step 3: Use glob to find all text files in the directory.
        file_paths = glob.glob(os.path.join(data_dir, '*.txt'))
        arr = []
        for iii in range(0,len(file_paths)):
            arr.append(int(file_paths[iii][5:len(file_paths[iii])-4]))
        
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
        
        # Step 4: Read and preprocess the data.
        data, labels = read_and_preprocess_data(file_paths)
        
        # text_rec = 'this is custom voice'
        lent = (text_rec.split(' '))
        for itrn in range(0,len(lent)):
                
            reviews = lent[itrn]
            default_ans = data
            
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            cosine_sim = []
            for ii in range(0,len(data)):
                
                # Two strings to compare
                string1 = default_ans[ii]
                string2 = reviews
                
                # Initialize the TF-IDF vectorizer
                vectorizer = TfidfVectorizer()
                
                # Transform the strings into TF-IDF vectors
                tfidf_matrix = vectorizer.fit_transform([string1, string2])
                
                # Calculate the cosine similarity between the vectors
                cosine_sim.append(cosine_similarity(tfidf_matrix[0], tfidf_matrix[1]))
                res = np.max(cosine_sim)

            print("Cosine Similarity:", cosine_sim)
            
            try:
                
                IDX.append(cosine_sim.index(res))
            except:
                IDX = cosine_sim.index(res)
        # =======================

            if res != 1:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(lent[itrn])
                engine.runAndWait()
            else:
                
                from pydub import AudioSegment
                from pydub.playback import play
                import noisereduce as nr
                
                import streamlit as st
                    
            
                audio = AudioSegment.from_file("Me/"+str(arr[IDX[itrn]])+".wav", format="wav")
                octaves = 0.9
                new_audio = audio.speedup(playback_speed=1.3 / octaves)
                
                temp_wav = "temp_output.wav"
                new_audio.export(temp_wav, format="wav")
                st.audio(temp_wav)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        try:
            import pyttsx3
            engine = pyttsx3.init()
            if 'text_rec' in locals():
                engine.say(text_rec)
                engine.runAndWait()
        except:
            pass


# ==========================================================================


if option == 'Person2':
    try:
        
        st.success(' Ready to record! Speak clearly when recording starts.')
    
        
        # Define the audio parameters
        FORMAT = pyaudio.paInt16  # Audio format
        CHANNELS = 1  # Mono audio
        RATE = 44100  # Sample rate (samples per second)
        CHUNK = 1024  # Size of each audio chunk
        RECORD_SECONDS = 5  # Duration of recording in seconds
        OUTPUT_FILENAME = "output.wav"  # Name of the output .wav file
        
        # Initialize the audio stream
        audio = pyaudio.PyAudio()
        
        # Create an audio stream
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        
        print("Recording...")
        st.text("Recording...")
        
        frames = []
        
        # Capture audio data
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        print("Finished recording.")
        st.text("Finished recording....")
        
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
        st.write(f"Audio saved as {OUTPUT_FILENAME}")
        
        # Convert speech to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(OUTPUT_FILENAME) as source:
            audio_data = recognizer.record(source)
            try:
                text_rec = recognizer.recognize_google(audio_data)
                print(f"Recognized text: {text_rec}")
                st.write(f"Recognized text: {text_rec}")
                
                # Write the recognized text to a Notepad file
                with open('test text/1.txt', 'w') as notepad:
                    notepad.write(text_rec)
                
                print(f"Recognized text saved in {'1.txt'}")
                st.write(f"Recognized text saved in {'1.txt'}")
                
                
            except sr.UnknownValueError:
                print("Could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
        
        # You can now use the 'text' variable containing the recognized text as needed.
        
        import numpy as np
        
        # =======================
        import glob# Step 2: Specify the directory containing your text files.
        
        import numpy as np

                        
        
        import os
        import glob
        from sklearn.model_selection import train_test_split
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.metrics import accuracy_score
        
        data_dir = 'Text/'
        IDX = []
        # Step 3: Use glob to find all text files in the directory.
        file_paths = glob.glob(os.path.join(data_dir, '*.txt'))
        arr = []
        for iii in range(0,len(file_paths)):
            arr.append(int(file_paths[iii][5:len(file_paths[iii])-4]))
        
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
        
        # Step 4: Read and preprocess the data.
        data, labels = read_and_preprocess_data(file_paths)
        
        # text_rec = 'this is custom voice'
        lent = (text_rec.split(' '))
        for itrn in range(0,len(lent)):
                
            reviews = lent[itrn]
            default_ans = data
            
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            cosine_sim = []
            for ii in range(0,len(data)):
                
                # Two strings to compare
                string1 = default_ans[ii]
                string2 = reviews
                
                # Initialize the TF-IDF vectorizer
                vectorizer = TfidfVectorizer()
                
                # Transform the strings into TF-IDF vectors
                tfidf_matrix = vectorizer.fit_transform([string1, string2])
                
                # Calculate the cosine similarity between the vectors
                cosine_sim.append(cosine_similarity(tfidf_matrix[0], tfidf_matrix[1]))
                res = np.max(cosine_sim)

            print("Cosine Similarity:", cosine_sim)
            
            try:
                
                IDX.append(cosine_sim.index(res))
            except:
                IDX = cosine_sim.index(res)
        # =======================

            if res != 1:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(lent[itrn])
                engine.runAndWait()
            else:
                
                from pydub import AudioSegment
                from pydub.playback import play
                import noisereduce as nr
                
                import streamlit as st
                    
            
                audio = AudioSegment.from_file("p2/"+str(arr[IDX[itrn]])+".wav", format="wav")
                octaves = 0.9
                new_audio = audio.speedup(playback_speed=1.3 / octaves)
                
                temp_wav = "temp_output.wav"
                new_audio.export(temp_wav, format="wav")
                st.audio(temp_wav)
    except:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text_rec)
        engine.runAndWait()
# ============================================================================= 
if option == 'Person3':
    try:
        
        st.success(' Ready to record! Speak clearly when recording starts.')
    
        
        # Define the audio parameters
        FORMAT = pyaudio.paInt16  # Audio format
        CHANNELS = 1  # Mono audio
        RATE = 44100  # Sample rate (samples per second)
        CHUNK = 1024  # Size of each audio chunk
        RECORD_SECONDS = 5  # Duration of recording in seconds
        OUTPUT_FILENAME = "output.wav"  # Name of the output .wav file
        
        # Initialize the audio stream
        audio = pyaudio.PyAudio()
        
        # Create an audio stream
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        
        print("Recording...")
        st.text("Recording...")
        
        frames = []
        
        # Capture audio data
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        print("Finished recording.")
        st.text("Finished recording....")
        
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
        st.write(f"Audio saved as {OUTPUT_FILENAME}")
        
        # Convert speech to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(OUTPUT_FILENAME) as source:
            audio_data = recognizer.record(source)
            try:
                text_rec = recognizer.recognize_google(audio_data)
                print(f"Recognized text: {text_rec}")
                st.write(f"Recognized text: {text_rec}")
                
                # Write the recognized text to a Notepad file
                with open('test text/1.txt', 'w') as notepad:
                    notepad.write(text_rec)
                
                print(f"Recognized text saved in {'1.txt'}")
                st.write(f"Recognized text saved in {'1.txt'}")
                
                
            except sr.UnknownValueError:
                print("Could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
        
        # You can now use the 'text' variable containing the recognized text as needed.
        
        import numpy as np
        
        # =======================
        import glob# Step 2: Specify the directory containing your text files.
        
        import numpy as np

                        
        
        import os
        import glob
        from sklearn.model_selection import train_test_split
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.metrics import accuracy_score
        
        data_dir = 'Text/'
        IDX = []
        # Step 3: Use glob to find all text files in the directory.
        file_paths = glob.glob(os.path.join(data_dir, '*.txt'))
        arr = []
        for iii in range(0,len(file_paths)):
            arr.append(int(file_paths[iii][5:len(file_paths[iii])-4]))
        
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
        
        # Step 4: Read and preprocess the data.
        data, labels = read_and_preprocess_data(file_paths)
        
        # text_rec = 'this is custom voice'
        lent = (text_rec.split(' '))
        for itrn in range(0,len(lent)):
                
            reviews = lent[itrn]
            default_ans = data
            
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            cosine_sim = []
            for ii in range(0,len(data)):
                
                # Two strings to compare
                string1 = default_ans[ii]
                string2 = reviews
                
                # Initialize the TF-IDF vectorizer
                vectorizer = TfidfVectorizer()
                
                # Transform the strings into TF-IDF vectors
                tfidf_matrix = vectorizer.fit_transform([string1, string2])
                
                # Calculate the cosine similarity between the vectors
                cosine_sim.append(cosine_similarity(tfidf_matrix[0], tfidf_matrix[1]))
                res = np.max(cosine_sim)

            print("Cosine Similarity:", cosine_sim)
            
            try:
                
                IDX.append(cosine_sim.index(res))
            except:
                IDX = cosine_sim.index(res)
        # =======================

            if res != 1:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(lent[itrn])
                engine.runAndWait()
            else:
                
                from pydub import AudioSegment
                from pydub.playback import play
                import noisereduce as nr
                
                import streamlit as st
                    
            
                audio = AudioSegment.from_file("p3/"+str(arr[IDX[itrn]])+".wav", format="wav")
                octaves = 0.9
                new_audio = audio.speedup(playback_speed=1.3 / octaves)
                
                temp_wav = "temp_output.wav"
                new_audio.export(temp_wav, format="wav")
                st.audio(temp_wav)
    except:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text_rec)
        engine.runAndWait()



# ============================================================================= 
if option == 'Person4':
    try:
        
        st.success(' Ready to record! Speak clearly when recording starts.')
    
        
        # Define the audio parameters
        FORMAT = pyaudio.paInt16  # Audio format
        CHANNELS = 1  # Mono audio
        RATE = 44100  # Sample rate (samples per second)
        CHUNK = 1024  # Size of each audio chunk
        RECORD_SECONDS = 5  # Duration of recording in seconds
        OUTPUT_FILENAME = "output.wav"  # Name of the output .wav file
        
        # Initialize the audio stream
        audio = pyaudio.PyAudio()
        
        # Create an audio stream
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        
        print("Recording...")
        st.text("Recording...")
        
        frames = []
        
        # Capture audio data
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        print("Finished recording.")
        st.text("Finished recording....")
        
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
        st.write(f"Audio saved as {OUTPUT_FILENAME}")
        
        # Convert speech to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(OUTPUT_FILENAME) as source:
            audio_data = recognizer.record(source)
            try:
                text_rec = recognizer.recognize_google(audio_data)
                print(f"Recognized text: {text_rec}")
                st.write(f"Recognized text: {text_rec}")
                
                # Write the recognized text to a Notepad file
                with open('test text/1.txt', 'w') as notepad:
                    notepad.write(text_rec)
                
                print(f"Recognized text saved in {'1.txt'}")
                st.write(f"Recognized text saved in {'1.txt'}")
                
                
            except sr.UnknownValueError:
                print("Could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
        
        # You can now use the 'text' variable containing the recognized text as needed.
        
        import numpy as np
        
        # =======================
        import glob# Step 2: Specify the directory containing your text files.
        
        import numpy as np

                        
        
        import os
        import glob
        from sklearn.model_selection import train_test_split
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.metrics import accuracy_score
        
        data_dir = 'Text/'
        IDX = []
        # Step 3: Use glob to find all text files in the directory.
        file_paths = glob.glob(os.path.join(data_dir, '*.txt'))
        arr = []
        for iii in range(0,len(file_paths)):
            arr.append(int(file_paths[iii][5:len(file_paths[iii])-4]))
        
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
        
        # Step 4: Read and preprocess the data.
        data, labels = read_and_preprocess_data(file_paths)
        
        # text_rec = 'this is custom voice'
        lent = (text_rec.split(' '))
        for itrn in range(0,len(lent)):
                
            reviews = lent[itrn]
            default_ans = data
            
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            cosine_sim = []
            for ii in range(0,len(data)):
                
                # Two strings to compare
                string1 = default_ans[ii]
                string2 = reviews
                
                # Initialize the TF-IDF vectorizer
                vectorizer = TfidfVectorizer()
                
                # Transform the strings into TF-IDF vectors
                tfidf_matrix = vectorizer.fit_transform([string1, string2])
                
                # Calculate the cosine similarity between the vectors
                cosine_sim.append(cosine_similarity(tfidf_matrix[0], tfidf_matrix[1]))
                res = np.max(cosine_sim)

            print("Cosine Similarity:", cosine_sim)
            
            try:
                
                IDX.append(cosine_sim.index(res))
            except:
                IDX = cosine_sim.index(res)
        # =======================

            if res != 1:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(lent[itrn])
                engine.runAndWait()
            else:
                
                from pydub import AudioSegment
                from pydub.playback import play
                import noisereduce as nr
                
                import streamlit as st
                    
            
                audio = AudioSegment.from_file("p4/"+str(arr[IDX[itrn]])+".wav", format="wav")
                octaves = 0.9
                new_audio = audio.speedup(playback_speed=1.3 / octaves)
                
                temp_wav = "temp_output.wav"
                new_audio.export(temp_wav, format="wav")
                st.audio(temp_wav)
    except:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text_rec)
        engine.runAndWait()
