# 🎙️ Custom Voice Cloner

A Streamlit application that combines voice cloning with text-to-speech to create natural-sounding audio output. Speak any sentence and hear it back using pre-recorded voice samples for known words and Google Text-to-Speech for unknown words.

## Features

- Browser-based audio recording
- Speech-to-text conversion using Google Speech Recognition
- Exact word matching with voice sample library
- Automatic fallback to Google Text-to-Speech (gTTS) for unknown words
- Seamless audio combining for natural output
- Support for multiple voice profiles (4 different voices)

## How It Works

1. **Select a voice** - Choose from Person1, Person2, Person3, or Person4
2. **Record your speech** - Use the browser's audio recorder
3. **Automatic processing**:
   - Speech is converted to text
   - Each word is checked against the voice library
   - **Exact match found** → Uses cloned voice sample
   - **No match** → Uses Google Text-to-Speech
4. **Combined output** - All words are merged into seamless audio

### Example

**Input:** "hello beautiful world"
- "hello" exists in library → Cloned voice ✅
- "beautiful" not in library → gTTS 🔊
- "world" not in library → gTTS 🔊

**Output:** Natural-sounding audio combining both sources

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
├── Text/                 # Training text files
│   ├── 0.txt
│   ├── 1.txt
│   └── ...
├── Me/                   # Person1 voice samples
│   ├── 0.wav
│   ├── 1.wav
│   └── ...
├── p2/                   # Person2 voice samples
├── p3/                   # Person3 voice samples
└── p4/                   # Person4 voice samples
```

## Important Notes

- Audio files should be in WAV format
- Each audio file should correspond to a text file with the same number
- Text files should contain single words (lowercase) for exact matching
- The app uses exact word matching (case-insensitive)
- Unknown words are automatically spoken using Google Text-to-Speech
- Browser must support audio recording (modern browsers like Chrome, Firefox, Edge)

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
