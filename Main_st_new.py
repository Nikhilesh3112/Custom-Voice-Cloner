import os
import sys
import traceback
import pyaudio
import wave
import speech_recognition as sr
import streamlit as st
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import subprocess

# Set page configuration
st.set_page_config(
    page_title="Custom Voice Cloner",
    page_icon="🎙️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        max-width: 1000px;
        padding: 2rem;
    }
    .title {
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        background-color: #f8f9fa;
    }
    .success {
        color: #388E3C;
        font-weight: bold;
    }
    .info {
        color: #0288D1;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1 class='title'>🎙️ Custom Voice Cloner</h1>", unsafe_allow_html=True)
st.markdown("### Transform text to speech with custom voice profiles")

# App Description
with st.expander("ℹ️ About this App"):
    st.write("""
    This application allows you to convert text to speech using custom voice profiles. 
    Select a voice profile from the dropdown menu and follow the instructions to generate speech.
    
    ### Features:
    - Multiple voice profiles to choose from
    - Real-time speech synthesis
    - Easy-to-use interface
    - High-quality voice output
    
    ### How to use:
    1. Select a voice profile from the dropdown
    2. Enter your text or use the microphone to speak
    3. Click the 'Generate Speech' button
    4. Listen to the generated speech
    """)

# Try to import noisereduce but don't fail if not available
try:
    import noisereduce as nr
except ImportError:
    nr = None
    print("Note: noisereduce module not found. Noise reduction will be disabled.")

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_info(message):
    """Helper function for debug messages"""
    print(f"[DEBUG] {message}")

try:
    import pyaudio
    p = pyaudio.PyAudio()
    p.terminate()
except Exception as e:
    st.error(f"Audio initialization error: {str(e)}")
    print(f"Audio error details: {traceback.format_exc()}")

# Voice Profile Selection
st.markdown("## 🎤 Select a Voice Profile")
option = st.selectbox(
    'Choose from the available voice profiles:',
    ('Select here...', 'Person1', 'Person2', 'Person3', 'Person4'),
    help='Select a voice profile to use for text-to-speech generation.'
)

if option != 'Select here...':
    st.success(f'✅ You selected: {option}')
    st.markdown("---")
# agree = st.checkbox('Give Test Voice')

if option == 'Person1':
    try:
        debug_info("Person1 selected")
        
        st.markdown("## 🎙️ Person 1 Voice Profile")
        st.markdown("""
        <div class='card'>
            <p>This profile features a clear and professional voice suitable for various applications.</p>
            <p>🔊 <strong>Voice Characteristics:</strong> Neutral tone, medium pitch, clear enunciation</p>
            <p>🎯 <strong>Best for:</strong> Professional presentations, educational content, general use</p>
        </div>
        """, unsafe_allow_html=True)
    
        
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
        # Initialize text_rec with a default value
        text_rec = "default text"  # Default value in case recognition fails
        
        try:
            with sr.AudioFile(OUTPUT_FILENAME) as source:
                audio_data = recognizer.record(source)
                try:
                    text_rec = recognizer.recognize_google(audio_data)
                    print(f"Recognized text: {text_rec}")
                    st.write("Recognized text:", text_rec)
                    
                    # Ensure the test text directory exists
                    os.makedirs('test text', exist_ok=True)
                    
                    # Write the recognized text to a Notepad file
                    with open('test text/1.txt', 'w', encoding='utf-8') as notepad:
                        notepad.write(text_rec)
                    
                    st.success("Text recognized and saved successfully")
                    
                except sr.UnknownValueError:
                    st.warning("Could not understand audio")
                    text_rec = "could not understand audio"
                except sr.RequestError as e:
                    st.error(f"Could not request results; {e}")
                    text_rec = f"recognition error: {str(e)}"
                
                # Try to open the text file with default application
                try:
                    if os.name == 'nt':  # For Windows
                        os.startfile("test text/1.txt")
                    else:  # For macOS and Linux
                        import subprocess
                        subprocess.run(['xdg-open', "test text/1.txt"], check=False)
                except Exception as e:
                    print(f"Note: Could not open text file: {e}")
                    # Don't show error to user as it's not critical
                    
        except Exception as e:
            st.error(f"Error processing audio file: {e}")
            text_rec = "error processing audio file"
            debug_info(f"Audio processing error: {traceback.format_exc()}")
        
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
        
        # Ensure text_rec is a string before splitting
        if not isinstance(text_rec, str):
            text_rec = str(text_rec)
        lent = text_rec.split()  # split() without arguments handles multiple spaces
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
            st.text(IDX)
        # =======================

            if res != 1:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(lent[itrn])
                engine.runAndWait()
            else:
                
                try:
                    from pydub import AudioSegment
                    from pydub.playback import play
                    
                    # Get the current working directory
                    current_dir = os.getcwd()
                    debug_info(f"Current working directory: {current_dir}")
                    
                    # List all files in the current directory
                    debug_info("Files in current directory:")
                    for f in os.listdir('.'):
                        debug_info(f"- {f} (dir: {os.path.isdir(f)})")
                    
                    # Check if Me directory exists
                    me_dir = os.path.join(current_dir, 'Me')
                    if not os.path.exists(me_dir):
                        st.error(f"Error: 'Me' directory not found in {current_dir}")
                        debug_info(f"Creating 'Me' directory at {me_dir}")
                        os.makedirs(me_dir, exist_ok=True)
                    
                    # List contents of Me directory
                    debug_info("Contents of Me directory:")
                    if os.path.exists(me_dir):
                        for f in os.listdir(me_dir):
                            debug_info(f"- {f}")
                    
                    # Construct the audio file path
                    audio_file = os.path.join(me_dir, f"{arr[IDX[itrn]]}.wav")
                    debug_info(f"Attempting to play audio file: {audio_file}")
                    
                    # Check if file exists
                    if not os.path.exists(audio_file):
                        error_msg = f"Audio file not found: {audio_file}"
                        st.error(error_msg)
                        debug_info(error_msg)
                        debug_info(f"Current directory contents: {os.listdir('.')}")
                        debug_info(f"Me directory contents: {os.listdir(me_dir) if os.path.exists(me_dir) else 'Does not exist'}")
                        continue  # Skip to next iteration if file not found
                        
                    # Load and play the audio with error handling
                    try:
                        audio = AudioSegment.from_file(audio_file, format="wav")
                        debug_info(f"Successfully loaded audio file: {audio_file}")
                        debug_info(f"Audio duration: {len(audio) / 1000.0} seconds")
                        
                        # Change the pitch
                        octaves = 0.9
                        new_audio = audio.speedup(playback_speed=1.3 / octaves)
                        
                        # Save the audio to a temporary file for playback
                        temp_audio_path = "temp_output.wav"
                        new_audio.export(temp_audio_path, format="wav")
                        
                        # Display the audio player in Streamlit
                        st.audio(temp_audio_path, format='audio/wav')
                        
                        # Also play the audio directly
                        debug_info("Attempting to play audio...")
                        play(new_audio)
                        debug_info("Audio playback completed successfully")
                        
                    except Exception as audio_error:
                        error_msg = f"Error playing audio: {str(audio_error)}"
                        st.error(error_msg)
                        debug_info(error_msg)
                        debug_info(f"Error details: {traceback.format_exc()}")
                        
                        # Fallback to TTS if audio playback fails
                        debug_info("Attempting TTS fallback...")
                        try:
                            import pyttsx3
                            engine = pyttsx3.init()
                            engine.say("Playing audio response")
                            engine.runAndWait()
                        except Exception as tts_error:
                            debug_info(f"TTS fallback failed: {str(tts_error)}")
                    
                except Exception as e:
                    error_msg = f"Error playing audio: {str(e)}"
                    st.error(error_msg)
                    debug_info(error_msg)
                    debug_info(f"Error details: {traceback.format_exc()}")
                
                
                # # Save the modified audio to a new file
                # new_audio.export("Final_res.wav", format="wav")
                # st.audio("Final_res.wav")
    except Exception as e:
        error_msg = f"Error in processing: {str(e)}"
        if "noisereduce" in str(e):
            error_msg = "Noise reduction is not available. Please install noisereduce module for better audio quality."
        st.error(error_msg)
        print(f"Error details: {traceback.format_exc()}")
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say("An error occurred during voice processing")
            engine.runAndWait()
        except Exception as tts_error:
            debug_info(f"TTS Error: {str(tts_error)}")


# ==========================================================================


if option == 'Person2':
    try:
        debug_info("Person2 selected")
        
        st.markdown("## 🎙️ Person 2 Voice Profile")
        st.markdown("""
        <div class='card'>
            <p>This profile features a warm and friendly voice perfect for conversational applications.</p>
            <p>🔊 <strong>Voice Characteristics:</strong> Warm tone, slightly lower pitch, natural flow</p>
            <p>🎯 <strong>Best for:</strong> Customer service, storytelling, casual content</p>
        </div>
        """, unsafe_allow_html=True)
    
        
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
        # Initialize text_rec with a default value
        text_rec = "default text"  # Default value in case recognition fails
        
        try:
            with sr.AudioFile(OUTPUT_FILENAME) as source:
                audio_data = recognizer.record(source)
                try:
                    text_rec = recognizer.recognize_google(audio_data)
                    print(f"Recognized text: {text_rec}")
                    st.write("Recognized text:", text_rec)
                    
                    # Ensure the test text directory exists
                    os.makedirs('test text', exist_ok=True)
                    
                    # Write the recognized text to a Notepad file
                    with open('test text/1.txt', 'w', encoding='utf-8') as notepad:
                        notepad.write(text_rec)
                    
                    st.success("Text recognized and saved successfully")
                    
                except sr.UnknownValueError:
                    st.warning("Could not understand audio")
                    text_rec = "could not understand audio"
                except sr.RequestError as e:
                    st.error(f"Could not request results; {e}")
                    text_rec = f"recognition error: {str(e)}"
                
                # Try to open the text file with default application
                try:
                    if os.name == 'nt':  # For Windows
                        os.startfile("test text/1.txt")
                    else:  # For macOS and Linux
                        import subprocess
                        subprocess.run(['xdg-open', "test text/1.txt"], check=False)
                except Exception as e:
                    print(f"Note: Could not open text file: {e}")
                    # Don't show error to user as it's not critical
                    
        except Exception as e:
            st.error(f"Error processing audio file: {e}")
            text_rec = "error processing audio file"
            debug_info(f"Audio processing error: {traceback.format_exc()}")
        
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
        
        # Ensure text_rec is a string before splitting
        if not isinstance(text_rec, str):
            text_rec = str(text_rec)
        lent = text_rec.split()  # split() without arguments handles multiple spaces
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
            st.text(IDX)
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
                # filtered_audio = audio.low_pass_filter(0.01)
                
                
                # Change the pitch
                octaves = 0.9  # You can adjust this value to change the pitch
                new_audio = audio.speedup(playback_speed=1.3 / octaves)
                
                
                # Play the modified audio
                play(new_audio)
                
                
                # # Save the modified audio to a new file
                # new_audio.export("Final_res.wav", format="wav")
                # st.audio("Final_res.wav")
    except Exception as e:
        error_msg = f"Error in processing: {str(e)}"
        if "noisereduce" in str(e):
            error_msg = "Noise reduction is not available. Please install noisereduce module for better audio quality."
        st.error(error_msg)
        print(f"Error details: {traceback.format_exc()}")
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say("An error occurred during voice processing")
            engine.runAndWait()
        except Exception as tts_error:
            debug_info(f"TTS Error: {str(tts_error)}")
# ============================================================================= 
if option == 'Person3':
    try:
        debug_info("Person3 selected")
        
        st.markdown("## 🎙️ Person 3 Voice Profile")
        st.markdown("""
        <div class='card'>
            <p>This profile features an energetic and enthusiastic voice that captures attention.</p>
            <p>🔊 <strong>Voice Characteristics:</strong> Energetic tone, higher pitch, expressive delivery</p>
            <p>🎯 <strong>Best for:</strong> Marketing, entertainment, engaging presentations</p>
        </div>
        """, unsafe_allow_html=True)
    
        
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
        # Initialize text_rec with a default value
        text_rec = "default text"  # Default value in case recognition fails
        
        try:
            with sr.AudioFile(OUTPUT_FILENAME) as source:
                audio_data = recognizer.record(source)
                try:
                    text_rec = recognizer.recognize_google(audio_data)
                    print(f"Recognized text: {text_rec}")
                    st.write("Recognized text:", text_rec)
                    
                    # Ensure the test text directory exists
                    os.makedirs('test text', exist_ok=True)
                    
                    # Write the recognized text to a Notepad file
                    with open('test text/1.txt', 'w', encoding='utf-8') as notepad:
                        notepad.write(text_rec)
                    
                    st.success("Text recognized and saved successfully")
                    
                except sr.UnknownValueError:
                    st.warning("Could not understand audio")
                    text_rec = "could not understand audio"
                except sr.RequestError as e:
                    st.error(f"Could not request results; {e}")
                    text_rec = f"recognition error: {str(e)}"
                
                # Try to open the text file with default application
                try:
                    if os.name == 'nt':  # For Windows
                        os.startfile("test text/1.txt")
                    else:  # For macOS and Linux
                        import subprocess
                        subprocess.run(['xdg-open', "test text/1.txt"], check=False)
                except Exception as e:
                    print(f"Note: Could not open text file: {e}")
                    # Don't show error to user as it's not critical
                    
        except Exception as e:
            st.error(f"Error processing audio file: {e}")
            text_rec = "error processing audio file"
            debug_info(f"Audio processing error: {traceback.format_exc()}")
        
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
        
        # Ensure text_rec is a string before splitting
        if not isinstance(text_rec, str):
            text_rec = str(text_rec)
        lent = text_rec.split()  # split() without arguments handles multiple spaces
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
            st.text(IDX)
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
                # filtered_audio = audio.low_pass_filter(0.01)
                
                
                # Change the pitch
                octaves = 0.9  # You can adjust this value to change the pitch
                new_audio = audio.speedup(playback_speed=1.3 / octaves)
                
                
                # Play the modified audio
                play(new_audio)
                
                
                # # Save the modified audio to a new file
                # new_audio.export("Final_res.wav", format="wav")
                # st.audio("Final_res.wav")
    except Exception as e:
        error_msg = f"Error in processing: {str(e)}"
        if "noisereduce" in str(e):
            error_msg = "Noise reduction is not available. Please install noisereduce module for better audio quality."
        st.error(error_msg)
        print(f"Error details: {traceback.format_exc()}")
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say("An error occurred during voice processing")
            engine.runAndWait()
        except Exception as tts_error:
            debug_info(f"TTS Error: {str(tts_error)}")



# ============================================================================= 
if option == 'Person4':
    try:
        debug_info("Person4 selected")
        
        st.markdown("## 🎙️ Person 4 Voice Profile")
        st.markdown("""
        <div class='card'>
            <p>This profile features a calm and soothing voice ideal for relaxation content.</p>
            <p>🔊 <strong>Voice Characteristics:</strong> Calm tone, soft pitch, measured pace</p>
            <p>🎯 <strong>Best for:</strong> Meditation guides, relaxation content, bedtime stories</p>
        </div>
        """, unsafe_allow_html=True)
    
        
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
        # Initialize text_rec with a default value
        text_rec = "default text"  # Default value in case recognition fails
        
        try:
            with sr.AudioFile(OUTPUT_FILENAME) as source:
                audio_data = recognizer.record(source)
                try:
                    text_rec = recognizer.recognize_google(audio_data)
                    print(f"Recognized text: {text_rec}")
                    st.write("Recognized text:", text_rec)
                    
                    # Ensure the test text directory exists
                    os.makedirs('test text', exist_ok=True)
                    
                    # Write the recognized text to a Notepad file
                    with open('test text/1.txt', 'w', encoding='utf-8') as notepad:
                        notepad.write(text_rec)
                    
                    st.success("Text recognized and saved successfully")
                    
                except sr.UnknownValueError:
                    st.warning("Could not understand audio")
                    text_rec = "could not understand audio"
                except sr.RequestError as e:
                    st.error(f"Could not request results; {e}")
                    text_rec = f"recognition error: {str(e)}"
                
                # Try to open the text file with default application
                try:
                    if os.name == 'nt':  # For Windows
                        os.startfile("test text/1.txt")
                    else:  # For macOS and Linux
                        import subprocess
                        subprocess.run(['xdg-open', "test text/1.txt"], check=False)
                except Exception as e:
                    print(f"Note: Could not open text file: {e}")
                    # Don't show error to user as it's not critical
                    
        except Exception as e:
            st.error(f"Error processing audio file: {e}")
            text_rec = "error processing audio file"
            debug_info(f"Audio processing error: {traceback.format_exc()}")
        
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
        
        # Ensure text_rec is a string before splitting
        if not isinstance(text_rec, str):
            text_rec = str(text_rec)
        lent = text_rec.split()  # split() without arguments handles multiple spaces
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
            st.text(IDX)
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
                # filtered_audio = audio.low_pass_filter(0.01)
                
                
                # Change the pitch
                octaves = 0.9  # You can adjust this value to change the pitch
                new_audio = audio.speedup(playback_speed=1.3 / octaves)
                
                
                # Play the modified audio
                play(new_audio)
                
                
                # # Save the modified audio to a new file
                # new_audio.export("Final_res.wav", format="wav")
                # st.audio("Final_res.wav")
    except Exception as e:
        error_msg = f"Error in processing: {str(e)}"
        if "noisereduce" in str(e):
            error_msg = "Noise reduction is not available. Please install noisereduce module for better audio quality."
        st.error(error_msg)
        print(f"Error details: {traceback.format_exc()}")
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say("An error occurred during voice processing")
            engine.runAndWait()
        except Exception as tts_error:
            debug_info(f"TTS Error: {str(tts_error)}")
