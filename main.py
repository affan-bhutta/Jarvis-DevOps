import pyttsx3
import webbrowser
import datetime
import requests
import time
import os
import json
from client import ask_ai_openrouter  # Import from the new file

# ================== CONFIG ==================

NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")

MUSIC_LIBRARY = {
    "believer": "https://www.youtube.com/watch?v=7wtfhZwyrcc",
    "faded": "https://www.youtube.com/watch?v=60ItHLz5WEA",
    "shape of you": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    "despacito": "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
}

def listen():
    """Listen for voice command"""
    import speech_recognition as sr
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(" Listening... (speak now)")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        
        try:
            text = r.recognize_google(audio)
            print(f" You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print(" Could not understand audio")
            return None
        except sr.RequestError:
            print(" Speech service error")
            return None
        except Exception:
            return None

def ask_ai(question):
    """Answer questions"""
    try:
        answer = ask_ai_openrouter(question)
        if "Error" in answer or "error" in answer:
            # If API returns error, use local responses
            return get_local_response(question)
        return answer
    except Exception:
        return get_local_response(question)

def get_local_response(question):
    """Local responses when API fails"""
    return f"I can answer: '{question}'. But my API is currently unavailable. I can still open websites, play music, and tell time!"

# ================== SPEAK FUNCTION ==================

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception:
        print(f"[SPEAK]: {text}")

# ================== SIMPLE COMMAND PROCESSOR ==================

def process_command(command):
    """Simple direct command processor"""
    print(f"Command: {command}")
    
    # For opening websites
    if "open google" in command.lower():
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open youtube" in command.lower():
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open facebook" in command.lower():
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open spotify" in command.lower():
        speak("Opening Spotify")
        webbrowser.open("https://open.spotify.com")
    elif "open github" in command.lower():
        speak("Opening GitHub")
        webbrowser.open("https://github.com")
    elif "open docker" in command.lower():
        speak("Opening Docker")
        webbrowser.open("https://docker.com")
    elif "open netflix" in command.lower():
        speak("Opening Netflix")
        webbrowser.open("https://netflix.com")
    elif "open whatsapp" in command.lower():
        speak("Opening WhatsApp Web")
        webbrowser.open("https://web.whatsapp.com")
    
    # For playing music
    elif command.lower().startswith("play"):
        song = command.lower().replace("play", "").strip()
        if song in MUSIC_LIBRARY:
            speak(f"Playing {song}")
            webbrowser.open(MUSIC_LIBRARY[song])
        else:
            speak(f"Searching for {song}")
            search_url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}+music"
            webbrowser.open(search_url)
    
    # For news
    elif "news" in command.lower():
        get_news()
    
    # For time
    elif "time" in command.lower() or "what time" in command.lower():
        tell_time()
    
        # For notes - handles "note" command
    elif command.lower().startswith("note"):
        note_text = command.lower().replace("note", "").strip()
        create_note(note_text)
        print(f" Note saved: {note_text}")
    
    # ADD THIS - handles "make a note" or "create a note"
    elif "make a note" in command.lower() or "create a note" in command.lower():
        # Extract the note content
        if "and add" in command.lower():
            # Get text after "and add"
            note_text = command.lower().split("and add")[1].strip()
        else:
            # Get text after "note"
            note_text = command.lower().replace("make a note", "").replace("create a note", "").strip()
        
        # Add date if requested
        if "date" in command.lower():
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            note_text = f"{today}: {note_text}"
        
        create_note(note_text)
        speak(f"Note created: {note_text}")
        print(f" Note saved: {note_text}")
    
    # For AI questions (everything else)
    else:
        answer = ask_ai(command)
        speak(answer)
        print(f"AI: {answer}")

# ================== HANDLERS (keeping for news and time) ==================

def get_news():
    if not NEWS_API_KEY:
        speak("News feature not configured.")
        return

    try:
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        )
        if r.status_code == 200:
            for art in r.json().get("articles", [])[:5]:
                title = art["title"]
                print(title)
                speak(title)
    except Exception:
        speak("Unable to fetch news.")

def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")
    print(f"Time: {now}")

def create_note(details):
    with open("notes.txt", "a") as f:
        f.write(details + "\n")
    speak("Note saved.")
    print("Note saved:", details)

# ================== DRIVER ==================

if __name__ == "__main__":
    print("Jarvis starting...")
    speak("Jarvis initialized successfully.")
    
    print("\nChoose mode:")
    print("1. Voice")
    print("2. Text")
    
    mode = input("Enter 1 or 2: ").strip()
    
    if mode == "1":
        print("Voice mode - speak commands")
        while True:
            command = listen()
            if command:
                if "exit" in command or "quit" in command:
                    speak("Goodbye")
                    break
                process_command(command)
    
    else:
        print("Text mode - type commands")
        while True:
            command = input("You: ").strip()
            if command.lower() in ["exit", "quit", "bye"]:
                speak("Goodbye")
                break
            process_command(command)
    
    print("\nJarvis execution completed.")