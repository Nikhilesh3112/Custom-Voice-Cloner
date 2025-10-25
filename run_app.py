import pyaudio
import wave
import speech_recognition as sr
import streamlit as st
import os
import sys
from pydub import AudioSegment
from pydub.playback import play

def setup_audio():
    try:
        # Check if PyAudio can access the microphone
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        
        # Print available audio devices (for debugging)
        print("\n=== Available Audio Devices ===")
        for i in range(0, num_devices):
            device = p.get_device_info_by_host_api_device_index(0, i)
            print(f"Device {i}: {device['name']} (Input Channels: {device['maxInputChannels']})")
        
        return True
    except Exception as e:
        st.error(f"Audio initialization error: {str(e)}")
        return False

def record_audio(filename, duration=5):
    try:
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        
        audio = pyaudio.PyAudio()
        
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                          rate=RATE, input=True,
                          frames_per_buffer=CHUNK)
        
        st.info("Recording... Speak now!")
        frames = []
        
        for _ in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        st.success("Recording complete!")
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            
        return True
        
    except Exception as e:
        st.error(f"Recording error: {str(e)}")
        return False

def play_audio(filename):
    try:
        if not os.path.exists(filename):
            st.error(f"Audio file not found: {filename}")
            return False
            
        audio = AudioSegment.from_wav(filename)
        st.audio(filename)
        play(audio)
        return True
        
    except Exception as e:
        st.error(f"Playback error: {str(e)}")
        return False

def main():
    st.title("Voice Processing App")
    
    # Check audio setup
    if not setup_audio():
        st.warning("Audio initialization failed. Please check your microphone.")
    
    # Record button
    if st.button("Record Audio"):
        output_file = "recording.wav"
        if record_audio(output_file):
            st.audio(output_file)
            
            # Try to play a sample audio file
            st.subheader("Playing sample audio...")
            sample_file = os.path.join("Me", "1.wav")
            if os.path.exists(sample_file):
                play_audio(sample_file)
            else:
                st.warning("Sample audio file not found.")
    
    # Play sample audio
    if st.button("Play Sample Audio"):
        sample_file = os.path.join("Me", "1.wav")
        if os.path.exists(sample_file):
            play_audio(sample_file)
        else:
            st.error("Sample audio file not found.")
    
    # Display system information
    with st.expander("System Information"):
        st.write(f"Python version: {sys.version}")
        st.write(f"Current directory: {os.getcwd()}")
        st.write(f"Audio files in Me/: {len([f for f in os.listdir('Me') if f.endswith('.wav')])} files found")

if __name__ == "__main__":
    main()
