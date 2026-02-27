# 🎙️ Custom Voice Cloner

A Streamlit application that allows users to speak a sentence and hear it played back in a different person's voice using pre-recorded audio samples.

## Features

- Browser-based audio recording
- Speech-to-text conversion using Google Speech Recognition
- Word matching using TF-IDF vectorization
- Voice cloning using pre-recorded audio samples
- Support for multiple voice profiles

## How It Works

1. Select a person whose voice you want to use
2. Record your voice using the browser's audio recorder
3. The app converts your speech to text
4. Each word is matched with pre-recorded audio samples
5. The sentence is played back in the selected person's voice

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
- The app uses Google Speech Recognition API (requires internet connection)
- Browser must support audio recording (modern browsers like Chrome, Firefox, Edge)

## Limitations

- Maximum recording length depends on browser capabilities
- Speech recognition accuracy depends on audio quality and accent
- Requires internet connection for speech-to-text conversion

## Technologies Used

- **Streamlit** - Web framework
- **SpeechRecognition** - Speech-to-text conversion
- **scikit-learn** - TF-IDF vectorization and cosine similarity
- **pydub** - Audio manipulation
- **ffmpeg** - Audio processing backend

## License

This project is open source and available for educational purposes.
