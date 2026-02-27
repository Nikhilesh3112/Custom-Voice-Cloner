import tkinter as tk
import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio)
        input_text.delete(1.0, tk.END)  # Clear any previous text
        input_text.insert(tk.END, recognized_text)
    except sr.UnknownValueError:
        input_text.delete(1.0, tk.END)
        input_text.insert(tk.END, "Sorry, I couldn't understand that.")
    except sr.RequestError:
        input_text.delete(1.0, tk.END)
        input_text.insert(tk.END, "Could not request results. Check your internet connection.")

def respond():
    user_input = input_text.get(1.0, tk.END).strip()
    bot_response = "Bot: You said, " + user_input
    response_text.delete(1.0, tk.END)
    response_text.insert(tk.END, bot_response)

# Create a tkinter window
root = tk.Tk()
root.title("Voice-Based Bot")

# Create GUI components
listen_button = tk.Button(root, text="Listen", command=listen)
listen_button.pack()

input_text = tk.Text(root, height=2, width=30)
input_text.pack()

respond_button = tk.Button(root, text="Respond", command=respond)
respond_button.pack()

response_text = tk.Text(root, height=2, width=30)
response_text.pack()

# Start the tkinter main loop
root.mainloop()
