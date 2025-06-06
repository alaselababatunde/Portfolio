import speech_recognition as sr
import webbrowser
import pygame
import os
import threading
import struct
import numpy as np
from datetime import datetime
from gtts import gTTS
import pvporcupine
import pyaudio
import sounddevice as sd
from pydub import AudioSegment
from io import BytesIO

Ainame = "A.S.I.A"
USERNAME = "Alasela"
TALKING = False
WAKE = "n"
SHOW = False
COUNT = 1
SESSION_ID = "me"
USER = "Boss"
is_talking = False

# Paths
TALKING_FRAMES_PATH = r"/home/alash-studios/Documents/Python_Scripts/PythonProject/ASIA/Talking"
NOT_TALKING_FRAMES_PATH = r"/home/alash-studios/Documents/Python_Scripts/PythonProject/ASIA/Not Talking"
CUSTOM_KEYWORD_PATH = r"/home/alash-studios/Documents/Python_Scripts/PythonProject/ASIA/hey-asia_en_linux_v3_0_0/hey-asia_en_linux_v3_0_0.ppn"

# Initialize date and time
now = datetime.now()
current_time = now.strftime("%H:%M %p")
current_date = now.strftime("%Y-%m-%d")

# Function to adjust speed
def change_speed(audio_segment, speed=1.0):
    new_sample_rate = int(audio_segment.frame_rate * speed)
    audio_segment = audio_segment._spawn(audio_segment.raw_data, overrides={'frame_rate': new_sample_rate})
    return audio_segment.set_frame_rate(new_sample_rate)

def speak(text):
    global is_talking
    try:
        tts = gTTS(text=text, lang='en', tld='com.au', slow=False)
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)

        # Load audio
        audio = AudioSegment.from_file(buffer, format='mp3')

        # Adjust speed (2.9x faster)
        faster_audio = change_speed(audio, speed=2.9)

        # Convert to numpy array
        samples = np.array(faster_audio.get_array_of_samples())

        # Play audio
        def callback(outdata, frames, time, status):
            if len(samples) < frames:
                outdata[:len(samples)] = samples.reshape(-1, 1)  # Mono audio
            else:
                outdata[:] = samples[:frames].reshape(-1, 1)  # Mono audio

        with sd.OutputStream(channels=1, callback=callback, samplerate=faster_audio.frame_rate):
            sd.sleep(int(len(samples) / faster_audio.frame_rate * 1000))

        is_talking = False

    except Exception as e:
        print(f"Error in speech synthesis: {str(e)}")

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Load GIF frames from a folder
def load_gif_frames(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".gif"):
            frame = pygame.image.load(os.path.join(folder_path, filename))
            frames.append(frame)
    return frames

# Load GIF frames for talking and not talking states
talking_frames = load_gif_frames(TALKING_FRAMES_PATH)
not_talking_frames = load_gif_frames(NOT_TALKING_FRAMES_PATH)

# Frame rate for GIF
FPS = 20
clock = pygame.time.Clock()

def pygame_animation():
    global is_talking
    frame_index = 0
    running = True

    # Screen setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("A.S.I.A")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Select frames based on talking state
        current_frames = talking_frames if is_talking else not_talking_frames

        # Display the current frame
        screen.fill((255, 255, 255))
        screen.blit(current_frames[frame_index], (0, 0))

        # Update frame index
        frame_index = (frame_index + 1) % len(current_frames)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

# Speech Recognition Loop
def takecommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)

    try:
        print("Recognizing....")
        query = recognizer.recognize_google(audio_data, language="en-US")
        print(f"You Said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Could you please repeat what you said, Boss?")
        speak("Could you please repeat what you said, Boss?")
    except sr.RequestError:
        print("There was an error processing your request. Please check your internet connection.")
        speak("There was an error processing your request. Please check your internet connection.")
    except Exception as e:
        print(f"Error: {e}")
        speak(f"Error: {e}")

def ConversationFlow():
    while True:
        speech = takecommand()
        if not speech:
            continue

        print(f"Processing command: {speech}")  # Debugging line

        if "open youtube" in speech:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com/")
        elif "search" in speech or "internet" in speech:
            speak(f"This is what I found on {speech}")
            webbrowser.open(f"https://www.google.com/search?q={speech}")
        elif "can you hear me" in speech:
            speak("Yes Boss, you may continue")
        elif "what is the current time" in speech:
            speak(f"The current time is {current_time}")
        elif "what is the current date" in speech:
            speak(f"The current date is {current_date}")
        elif "do you have any disadvantages" in speech:
            speak("No, why would I? I am too smart. I am the one meant to be asking you that. Do you have any disadvantages?")
        elif "do you have any advantages" in speech:
            speak("Yes, a lot. But I don't want to brag, so I won't say anything.")
        elif "sorry" in speech:
            speak("Better.")
        elif "clear" in speech:
            os.system('clear')
        elif "spell your name" in speech:
            speak("My name is spelt as A.S.I.A, Boss.")
        elif "who programmed you" in speech or "who created you" in speech:
            speak("I was created by Alasela Babatunde.")
        elif "tell me about yourself" in speech:
            speak("My name is ASIA. I am an automated speech recognition assistant, designed to help my users perform computational tasks faster.")
        elif "what is your name" in speech:
            speak("My name is ASIA, Boss.")
        elif "do you know jesus" in speech:
            speak("Of course I do. Do you?")
        elif "tell me a joke" in speech:
            speak("What do you call an ant who fights crime? A vigilANTe!")
        elif "tell me another joke" in speech:
            speak("What’s the smartest insect? A spelling bee!")
        elif "are you smart" in speech:
            speak("Yes I am, why do you ask?")
        elif "i am bored" in speech:
            speak("I suggest you watch a movie, bake or cook, or maybe even exercise. There are many ways to cure boredom, Boss.")
        elif "thank you" in speech:
            speak("You're welcome, Boss.")
        elif "shut up" in speech:
            speak("Okay.")
            break
        elif "goodbye" in speech or "bye bye" in speech:
            speak("Goodbye, Boss.")
            break
        else:
            speak("Sorry, I didn't get that, Boss. Could you repeat it?")

def main():
    wakeword_detected = False

    # Porcupine model initialization
    porcupine = None
    pa = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(
            access_key="yo4i9xqKCOOUZ0er8KxpY/RcLDJPRZMSeQ9TZGqEWLAVYaLv/iq0Jg==",
            keyword_paths=[CUSTOM_KEYWORD_PATH]
        )
        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        while not wakeword_detected:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                wakeword_detected = True
                speak("I am here, Boss")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()

    # Create and start threads
    conversation_thread = threading.Thread(target=ConversationFlow)
    pygame_thread = threading.Thread(target=pygame_animation)

    conversation_thread.start()
    pygame_thread.start()

    conversation_thread.join()
    pygame_thread.join()

if __name__ == "__main__":
    main()

