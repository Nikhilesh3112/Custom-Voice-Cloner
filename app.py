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
import json
from datetime import datetime

# App Title and Description
st.set_page_config(page_title="Custom Voice Cloner", page_icon="🎙️")
st.title("🎙️ Custom Voice Cloner")

# Create tabs
tab1, tab2 = st.tabs(["🎤 Use Voice", "➕ Create Profile"])

# TAB 1: Use existing voice profiles
with tab1:
    st.markdown("""
    ### Use Voice Cloning
    Select a voice profile and speak a sentence to hear it in that person's voice.
    
    Choose from 4 pre-loaded voices or use your own custom profile created in the "Create Profile" tab.
    """)
    
    # Get available profiles
    available_profiles = ['Person1', 'Person2', 'Person3', 'Person4']
    
    # Check for custom profiles
    if os.path.exists('custom_profiles'):
        custom_dirs = [d for d in os.listdir('custom_profiles') if os.path.isdir(os.path.join('custom_profiles', d))]
        available_profiles.extend(custom_dirs)
    
    option = st.selectbox(
        '🎭 Select Voice Profile',
        ['Select here...'] + available_profiles,
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
    
    # Add custom profiles to mapping
    if option not in person_folder_map and option != 'Select here...':
        person_folder_map[option] = f'custom_profiles/{option}'

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
                        
                        # Load text data - check if custom profile or default
                        if option in ['Person1', 'Person2', 'Person3', 'Person4']:
                            data_dir = 'Text/'
                        else:
                            # Custom profile
                            data_dir = f'custom_profiles/{option}_text/'
                        
                        file_paths = glob.glob(os.path.join(data_dir, '*.txt'))
                        
                        if not file_paths:
                            st.error(f"No words found in {option}'s vocabulary. Please add words in the 'Create Profile' tab.")
                        else:
                            arr = []
                            for file_path in file_paths:
                                try:
                                    # Extract just the filename without extension
                                    filename = os.path.basename(file_path)
                                    index = int(filename.split('.')[0])
                                    arr.append(index)
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


# TAB 2: Create Voice Profile
with tab2:
    st.markdown("""
    ### Create Your Own Voice Profile
    Build your custom voice library by recording individual words.
    """)
    
    # Profile name input
    profile_name = st.text_input("📝 Profile Name", placeholder="e.g., MyVoice", key="profile_name")
    
    if profile_name:
        profile_path = f"custom_profiles/{profile_name}"
        text_path = f"custom_profiles/{profile_name}_text"
        
        # Create directories if they don't exist
        os.makedirs(profile_path, exist_ok=True)
        os.makedirs(text_path, exist_ok=True)
        
        st.success(f"✅ Profile: **{profile_name}**")
        
        # Show existing words in profile
        existing_files = glob.glob(os.path.join(text_path, '*.txt'))
        if existing_files:
            st.info(f"📚 Current vocabulary: {len(existing_files)} words")
            
            # Show word list
            with st.expander("View vocabulary"):
                words_list = []
                for file_path in sorted(existing_files):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        words_list.append(f.read().strip())
                st.write(", ".join(words_list))
        
        st.markdown("---")
        
        # Add new word section
        st.subheader("➕ Add New Word")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            new_word = st.text_input("Word to record", placeholder="e.g., hello", key="new_word")
        
        with col2:
            st.write("")
            st.write("")
        
        if new_word:
            new_word_lower = new_word.lower().strip()
            
            # Check if word already exists
            word_exists = False
            for file_path in existing_files:
                with open(file_path, 'r', encoding='utf-8') as f:
                    if f.read().strip().lower() == new_word_lower:
                        word_exists = True
                        st.warning(f"⚠️ Word '{new_word}' already exists in your vocabulary")
                        break
            
            if not word_exists:
                st.info(f"🎙️ Ready to record: **{new_word}**")
                
                # Audio recording
                audio_bytes = st.audio_input(f"Record yourself saying '{new_word}'", key=f"record_{new_word}")
                
                if audio_bytes:
                    try:
                        # Find next available index
                        existing_indices = []
                        for f in glob.glob(os.path.join(profile_path, '*.wav')):
                            try:
                                idx = int(os.path.basename(f).split('.')[0])
                                existing_indices.append(idx)
                            except:
                                pass
                        
                        next_idx = 0 if not existing_indices else max(existing_indices) + 1
                        
                        # Save audio file
                        audio_file_path = os.path.join(profile_path, f"{next_idx}.wav")
                        with open(audio_file_path, 'wb') as f:
                            f.write(audio_bytes.getvalue())
                        
                        # Save text file
                        text_file_path = os.path.join(text_path, f"{next_idx}.txt")
                        with open(text_file_path, 'w', encoding='utf-8') as f:
                            f.write(new_word_lower)
                        
                        st.success(f"✅ Added '{new_word}' to your profile!")
                        st.balloons()
                        st.info("💡 Tip: Clear the word field and add more words to build your vocabulary!")
                        
                    except Exception as e:
                        st.error(f"❌ Error saving word: {str(e)}")
        
        st.markdown("---")
        
        # Instructions
        with st.expander("📖 How to use your custom profile"):
            st.markdown("""
            1. **Add words** - Record yourself saying individual words
            2. **Build vocabulary** - Add as many words as you want
            3. **Use it** - Go to the "Use Voice" tab and select your profile
            4. **Speak sentences** - Any words in your vocabulary will use your voice!
            
            **Tips:**
            - Speak clearly when recording
            - Record in a quiet environment
            - Add common words you use frequently
            - You can add more words anytime
            """)
