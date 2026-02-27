# 🎙️ Custom Voice Cloner

A Streamlit application that allows you to speak a sentence and hear it played back in a different person's voice using pre-recorded audio samples.

## Features

- Browser-based audio recording
- Speech-to-text conversion using Google Speech Recognition
- Voice cloning using pre-recorded audio samples
- Automatic fallback for unknown words
- Support for multiple voice profiles (4 pre-loaded voices)
- **Create your own custom voice profile** - Record your own voice and build a personal vocabulary
- Easy-to-use interface with two tabs: Use Voice and Create Profile

## How It Works

### Using Pre-loaded Voices
1. **Select a voice** - Choose from Person1, Person2, Person3, Person4, or your custom profiles
2. **Record your speech** - Use the browser's audio recorder
3. **Automatic processing** - Speech is converted to text and played back in the selected voice
4. **Natural output** - Seamless audio combining for smooth playback

### Creating Your Own Voice Profile
1. **Go to "Create Profile" tab** - Click the second tab in the app
2. **Name your profile** - Enter a unique name for your voice profile
3. **Record words** - Type a word and record yourself saying it
4. **Build vocabulary** - Add as many words as you want to your personal library
5. **Use your voice** - Switch to "Use Voice" tab and select your custom profile
6. **Speak sentences** - Words in your vocabulary will use your voice, others use Google TTS

## Deployment to Streamlit Cloud

### Prerequisites

1. A GitHub account
2. Your voice sample files organized in folders:
   - `Me/` - Person1 voice samples
   - `p2/` - Person2 voice samples
   - `p3/` - Person3 voice samples
   - `p4/` - Person4 voice samples
3. Text files in `Text/` folder corresponding to each audio sample

### Steps to Deploy

1. **Create a GitHub Repository**
   - Go to GitHub and create a new repository
   - Name it something like "custom-voice-cloner"

2. **Upload Your Files**
   - Upload all files from this project to your GitHub repository:
     - `app.py` (main application)
     - `requirements.txt` (Python dependencies)
     - `packages.txt` (system dependencies)
     - `Text/` folder with all text files
     - `Me/`, `p2/`, `p3/`, `p4/` folders with audio samples

3. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set main file path to: `app.py`
   - Click "Deploy"

4. **Wait for Deployment**
   - Streamlit Cloud will install dependencies and start your app
   - This may take 5-10 minutes on first deployment

## Local Development

To run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## File Structure

```
.
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── packages.txt          # System dependencies (ffmpeg)
├── Text/                 # Training text files for pre-loaded voices
│   ├── 0.txt
│   ├── 1.txt
│   └── ...
├── Me/                   # Person1 voice samples
│   ├── 0.wav
│   ├── 1.wav
│   └── ...
├── p2/                   # Person2 voice samples
├── p3/                   # Person3 voice samples
├── p4/                   # Person4 voice samples
└── custom_profiles/      # User-created voice profiles (auto-generated)
    ├── {profile_name}/   # Audio files for custom profile
    └── {profile_name}_text/  # Text files for custom profile
```

## Important Notes

- Audio files should be in WAV format
- Each audio file should correspond to a text file with the same number (for pre-loaded voices)
- Text files should contain single words (lowercase) for exact matching
- The app uses exact word matching (case-insensitive)
- Unknown words are automatically spoken using Google Text-to-Speech
- Browser must support audio recording (modern browsers like Chrome, Firefox, Edge)
- Custom profiles are stored locally in the `custom_profiles/` directory
- You can create multiple custom profiles with different names
- Each custom profile maintains its own vocabulary independently

## Limitations

- Maximum recording length depends on browser capabilities
- Speech recognition accuracy depends on audio quality and accent
- Requires internet connection for speech-to-text conversion

## Technologies Used

- **Streamlit** - Web framework
- **SpeechRecognition** - Speech-to-text conversion
- **gTTS (Google Text-to-Speech)** - Fallback for unknown words
- **pydub** - Audio manipulation and combining
- **ffmpeg** - Audio processing backend
- **scikit-learn** - Text preprocessing (no longer used for matching)

## License

This project is open source and available for educational purposes.
