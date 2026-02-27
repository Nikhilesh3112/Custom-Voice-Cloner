import wave
import speech_recognition as sr
import streamlit as st
import numpy as np
import os
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pydub import AudioSegment
import tempfile
from gtts import gTTS

# App Title and Description
st.set_page_config(page_title="Custom Voice Cloner", page_icon="🎙️")
st.title("🎙️ Custom Voice Cloner")
st.markdown("""
### Welcome to Custom Voice Cloner!
This application allows you to speak a sentence and hear it played back in a different person's voice.

**How it works:**
1. Select a person whose voice you want to use
2. Record your voice using the audio recorder below
3. Your speech is converted to text
4. Each word is matched with pre-recorded audio samples
5. The sentence is played back in the selected person's voice

---
""")

option = st.selectbox(
    '🎭 Select Person Voice',
    ('Select here...','Person1', 'Person2', 'Person3','Person4'),
    key='person_selector')

if option != 'Select here...':
    st.info(f'You selected: **{option}**')

# Map person to folder
person_folder_map = {
    'Person1': 'Me',
    'Person2': 'p2',
    'Person3': 'p3',
    'Person4': 'p4'
}

if option != 'Select here...':
    st.success('✅ Ready to record! Click the microphone button below and speak clearly.')
    
    # Create a container for dynamic content
    output_container = st.container()
    
    # Browser-based audio recording
    audio_bytes = st.audio_input("🎤 Record your voice", key=f"audio_input_{option}")
    
    if audio_bytes:
        with output_container:
            try:
                # Save uploaded audio to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    tmp_file.write(audio_bytes.getvalue())
                    audio_path = tmp_file.name
                
                st.write("✅ Audio received! Processing...")
                
                # Convert speech to text
                recognizer = sr.Recognizer()
                with sr.AudioFile(audio_path) as source:
                    audio_data = recognizer.record(source)
                    try:
                        text_rec = recognizer.recognize_google(audio_data)
                        st.write(f"**Recognized text:** {text_rec}")
                        
                        # Load text data
                        data_dir = 'Text/'
                        file_paths = glob.glob(os.path.join(data_dir, '*.txt'))
                        
                        if not file_paths:
                            st.error("No training text files found in Text/ directory")
                        else:
                            arr = []
                            for file_path in file_paths:
                                try:
                                    arr.append(int(file_path[5:len(file_path)-4]))
                                except:
                                    pass
                            
                            # Read and preprocess data - create a word-to-index mapping
                            def read_and_preprocess_data(file_paths):
                                data = []
                                word_to_index = {}
                                for i, file_path in enumerate(file_paths):
                                    with open(file_path, 'r', encoding='utf-8') as file:
                                        content = file.read().strip().lower()
                                        data.append(content)
                                        word_to_index[content] = i
                                return data, word_to_index
                            
                            data, word_to_index = read_and_preprocess_data(file_paths)
                            
                            # Process each word - use exact matching
                            words = text_rec.split(' ')
                            word_matches = []
                            
                            st.write(f"**Processing {len(words)} word(s)...**")
                            
                            for word in words:
                                word_lower = word.lower().strip()
                                
                                # Check for exact match
                                if word_lower in word_to_index:
                                    # Exact match found - use cloned voice
                                    word_matches.append({
                                        'word': word,
                                        'use_cloned': True,
                                        'index': word_to_index[word_lower]
                                    })
                                else:
                                    # No match - use gTTS
                                    word_matches.append({
                                        'word': word,
                                        'use_cloned': False,
                                        'index': None
                                    })
                            
                                similarity_scores.append(max_similarity)
                            
                            # Get selected person's folder
                            person_folder = person_folder_map[option]
                            
                            # Check if folder exists
                            if not os.path.exists(person_folder):
                                st.error(f"Voice folder '{person_folder}' not found!")
                            else:
                                # Combine audio files
                                combined_audio = None
                                tts_words = []
                                cloned_words = []
                                
                                for match in word_matches:
                                    word = match['word']
                                    
                                    if match['use_cloned']:
                                        # Use cloned voice
                                        idx = match['index']
                                        audio_file = f"{person_folder}/{arr[idx]}.wav"
                                        
                                        if os.path.exists(audio_file):
                                            cloned_words.append(word)
                                            audio_segment = AudioSegment.from_file(audio_file, format="wav")
                                            
                                            # Apply pitch and speed adjustment
                                            octaves = 0.9
                                            new_audio = audio_segment.speedup(playback_speed=1.3 / octaves)
                                            
                                            if combined_audio is None:
                                                combined_audio = new_audio
                                            else:
                                                combined_audio += new_audio
                                        else:
                                            # File doesn't exist, use gTTS
                                            tts_words.append(word)
                                            try:
                                                tts = gTTS(text=word, lang='en', slow=False)
                                                tts_file = f"tts_{word}.mp3"
                                                tts.save(tts_file)
                                                tts_audio = AudioSegment.from_mp3(tts_file)
                                                
                                                if combined_audio is None:
                                                    combined_audio = tts_audio
                                                else:
                                                    combined_audio += tts_audio
                                                
                                                os.unlink(tts_file)
                                            except Exception as e:
                                                st.warning(f"Could not generate TTS for '{word}': {str(e)}")
                                    else:
                                        # Use gTTS for non-matching words
                                        tts_words.append(word)
                                        try:
                                            tts = gTTS(text=word, lang='en', slow=False)
                                            tts_file = f"tts_{word}.mp3"
                                            tts.save(tts_file)
                                            tts_audio = AudioSegment.from_mp3(tts_file)
                                            
                                            if combined_audio is None:
                                                combined_audio = tts_audio
                                            else:
                                                combined_audio += tts_audio
                                            
                                            os.unlink(tts_file)
                                        except Exception as e:
                                            st.warning(f"Could not generate TTS for '{word}': {str(e)}")
                                
                                if combined_audio:
                                    # Export combined audio
                                    output_path = "output_combined.wav"
                                    combined_audio.export(output_path, format="wav")
                                    
                                    st.success("✅ Voice cloning complete!")
                                    st.audio(output_path)
                                else:
                                    st.error("❌ Could not generate audio. Voice samples may be missing.")
                    
                    except sr.UnknownValueError:
                        st.error("❌ Could not understand the audio. Please speak clearly and try again.")
                    except sr.RequestError as e:
                        st.error(f"❌ Could not request results from speech recognition service: {e}")
                
                # Clean up temp file
                try:
                    os.unlink(audio_path)
                except:
                    pass
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
