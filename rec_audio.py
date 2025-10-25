import pyaudio
import wave

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
