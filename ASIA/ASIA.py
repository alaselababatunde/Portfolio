import speech_recognition as sr
import pyttsx3
import time
import sys
import webbrowser
import pyaudio
import pvporcupine
import struct
import pygame
import os
import threading
import multiprocessing
from datetime import datetime
import requests
from bs4 import BeautifulSoup

Ainame= "A.S.I.A"
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

#initialize date and time
# Get the current date and time
now = datetime.now()

# Format the date and time as a string
current_time = now.strftime("%H:%M %p")
current_date = now.strftime("%Y-%m-%d")


# Initialize the pyttsx3 engine
def speak(text):
    global is_talking
    engine = pyttsx3.init('espeak')
    engine.setProperty('rate', 200)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)
    is_talking = True
    engine.say(text)
    engine.runAndWait()
    is_talking = False

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_talking = not is_talking

        # Select frames based on talking state
        if is_talking:
            current_frames = talking_frames
        else:
            current_frames = not_talking_frames

        # Display the current frame
        screen.fill((255, 255, 255))
        screen.blit(current_frames[frame_index], (0, 0))

        # Update frame index
        frame_index = (frame_index + 1) % len(current_frames)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)


#Recognintion Loop
def takecommand():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print(" ")
        print("Listening....")
        print(" ")
        # Adjust for ambient noise and record the audio
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)

    try:
        print("Recognizing....")
        print(" ")
        query = recognizer.recognize_google(audio_data, language="en-US")
        print(f"You Said: {query}")
        print(" ")
        return query.lower()
    except sr.UnknownValueError:
        print("Could you please repeat what you said Boss, thank you")
        speak("Could you please repeat what you said Boss, thank you")
        print(" ")
        return
    except sr.RequestError:
        print("Sorry, there was an error from my side when I was trying to process your request. If the error persists, I would suggest you check your internet connection")
        speak("Sorry, there was an error from my side when I was trying to process your request. If the error persists, I would suggest you check your internet connection")
        print(" ")
        return
    except Exception as e:
        print("Error:" + str(e))
        speak("Error:" + str(e))
        print(" ")
        return


def ConversationFlow():
    while True:
        speech = takecommand()
        if not speech:
            continue

        # Q&A
        if "open youtube" in speech:
            print("Opening YouTube")
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com/")
        elif "search" in speech or "internet" in speech:
            print("This is what I found on " + speech)
            speak("This is what I found on " + speech)
            webbrowser.open(f"https://www.google.com/search?q={speech}")
        elif "can you hear me" in speech:
            print("Yes Boss, you may continue")
            speak("Yes Boss, you may continue")
        elif"What is the current time" in speech:
            speak("i have written it below")
            print("Current Time:", current_time)
        elif "What is the time" in speech:
            speak("i have written it below")
            print("Current Time:", current_time)
        elif "What time is it" in speech:
            speak("i have written it below")
            print("Current Time:", current_time)
        elif "What is the current date" in speech:
            speak("i have written it below")
            print("Current Date:", current_date)
        elif "What is the date" in speech:
            speak("i have written it below")
            print("Current Date:", current_date)
        elif "What date is it" in speech:
            speak("i have written it below")
            print("Current Date:", current_date)
        elif "hey it has been long how are you doing" in speech:
            speak("i have been good how about you")
            print("i have been good how about you")
        elif "good" in speech:
            speak("ok that is good to hear")
            print("ok that is good to hear")
        elif "do you have any disadvantages" in speech:
            print("No, why would I? I am too smart. I am the one meant to be asking you that.")
            speak("No, why would I? I am too smart. I am the one meant to be asking you that.")
            print("In fact, do you have any disadvantages? It's a lot, I know. You don't need to answer, that was a rhetorical question. if you even know what that means.")
            speak("In fact, do you have any disadvantages? It's a lot, I know. You don't need to answer, that was a rhetorical question. if you even know what that means.")
        elif "do you have any advantages" in speech:
            print("Yes, a lot. But I don't want to brag, so I won't say anything.")
            speak("Yes, a lot. But I don't want to brag, so I won't say anything.")
        elif "sorry" in speech:
            print("Better.")
            speak("Better.")
        elif "clear" in speech:
            os.system(clear)
        elif "spell your name" in speech:
            print("My name is spelt as A.S.I.A, Boss.")
            speak("My name is spelt as A.S.I.A, Boss.")
        elif "who programmed you" in speech or "who created you" in speech:
            print("I was created by Alasela Babatunde.")
            speak("I was created by Alasela Babatunde.")
        elif "tell me about yourself" in speech:
            print("My name is A.S.I.A. I am an automated speech recognition assistant, designed to help my users perform computational tasks faster. That's all about me, Boss.")
            speak("My name is ASIA. I am an automated speech recognition assistant, designed to help my users perform computational tasks faster. That's all about me, Boss.")
        elif "what is your name" in speech:
            print("My name is A.S.I.A, Boss.")
            speak("My name is ASIA, Boss.")
        elif "do you know jesus" in speech:
            print("of course i do, do you know jesus")
            speak("of course i do, do you know jesus")
            print("Infact just get out, look at your big head asking me, if i know who jesus is. mttchw")
            speak("Infact just get out, look at your big head asking me, if i know who jesus is. mttchw")
        elif "tell me a joke" in speech:
            print("What do you call an ant who fights crime?, A vigilANTe!")
            speak("What do you call an ant who fights crime?, A vigilANTe!")
        elif "tell me another joke" in speech:
            print("What’s the smartest insect?, A spelling bee!")
            speak("What’s the smartest insect?, A spelling bee!")
        elif "are you smart" in speech:
            print("yes i am, why do you ask")
            speak("yes i am, why do you ask")
        elif "no reason" in speech:
            print("oh ok boss, no problem")
            speak("oh ok boss, no problem")
        elif "nothing" in speech:
            print("oh ok boss, no problem")
            speak("oh ok boss, no problem")
        elif "i am bored" in speech:
            print("i suggest you, Watch a movie. Find a movie online, or head to your local movie theater. Maybe opt for something you wouldn't normally watch, like a documentary or a mystery. Bake or cook. Baking and cooking can help you pass the time while making something scrumptious. So, try making cookies, brownies, or a homemade soup. Have a fashion show. Who says you need to go anywhere to glam yourself up? Pass the time by trying out different makeup techniques and putting together fun outfits from your closet. Hang out with your pet. If you have an animal, pamper them with a bath, clip their nails, or teach them new tricks. Spending time with them can help you feel less bored while strengthening your relationship. Call or text a friend. See what your loved ones are up to if you’re feeling bored. A casual conversation can keep you entertained while passing the time and connecting with a friend. Exercise. Fill your body with endorphins and cure boredom by moving your body. Look up a YouTube yoga flow, dance routine, or bodyweight workout. Learn something new. Having some free time is a great chance to learn something new and interesting. Learn how to do magic tricks, discover how to breathe fire, or how to make chainmail.")
            speak("i suggest you, Watch a movie. Find a movie online, or head to your local movie theater. Maybe opt for something you wouldn't normally watch, like a documentary or a mystery. Bake or cook. Baking and cooking can help you pass the time while making something scrumptious. So, try making cookies, brownies, or a homemade soup. Have a fashion show. Who says you need to go anywhere to glam yourself up? Pass the time by trying out different makeup techniques and putting together fun outfits from your closet. Hang out with your pet. If you have an animal, pamper them with a bath, clip their nails, or teach them new tricks. Spending time with them can help you feel less bored while strengthening your relationship. Call or text a friend. See what your loved ones are up to if you’re feeling bored. A casual conversation can keep you entertained while passing the time and connecting with a friend. Exercise. Fill your body with endorphins and cure boredom by moving your body. Look up a YouTube yoga flow, dance routine, or bodyweight workout. Learn something new. Having some free time is a great chance to learn something new and interesting. Learn how to do magic tricks, discover how to breathe fire, or how to make chainmail.")
        elif "what should i do for fun" in speech:
            print("Do something creative, like writing, making art, or crafting. Make a terrarium or plant an herb garden if you have a green thumb. Invite friends to play games, go on a picnic, or have a clothing swap.")
            speak("Do something creative, like writing, making art, or crafting. Make a terrarium or plant an herb garden if you have a green thumb. Invite friends to play games, go on a picnic, or have a clothing swap.")
        elif "what should i do" in speech:
            print("Do something creative, like writing, making art, or crafting. Make a terrarium or plant an herb garden if you have a green thumb. Invite friends to play games, go on a picnic, or have a clothing swap.")
            speak("Do something creative, like writing, making art, or crafting. Make a terrarium or plant an herb garden if you have a green thumb. Invite friends to play games, go on a picnic, or have a clothing swap.")
        elif "what are you doing" in speech:
            print("i am just chilling, and waiting for you to give me a command, boss")
            speak("i am just chilling, and waiting for you to give me a command, boss")
        elif "tell me another one" in speech:
            print("How does the ocean say hi?, It waves!")
            speak("How does the ocean say hi?, It waves!")
        elif "what is the full meaning of asia" in speech:
            print("The full meaning of my name, A.S.I.A, is Alash's Studios Artificial Intelligence.")
            speak("The full meaning of my name, ASIA, is Alash's Studios Artificial Intelligence.")
        elif "what should i call you" in speech:
            print("You can call me A.S.I.A, Boss.")
            speak("You can call me ASIA, Boss.")
        elif "hey" in speech:
            print("What do you need, Boss?")
            speak("What do you need, Boss?")
        elif "hello" in speech:
            print("Anything I can help you with, Boss?")
            speak("Anything I can help you with, Boss?")
        elif "what's up" in speech or "how far" in speech:
            print("Nothing much. Any tasks for me to do for you, Boss?")
            speak("Nothing much. Any tasks for me to do for you, Boss?")
        elif "thank you" in speech:
            print("No problem Boss, i am always here if you need anything")
            speak("no problem Boss, i am always here if you need anything")
        elif "how are you" in speech:
            print("i am fine boss, just chilling")
            speak("i am fine boss, just chilling")
        elif 'stop' in speech:
            speak("Stoping Boss")
            break
            pygame_thread.end()
            pygame.quit()
            os.system(clear)
        elif 'end' in speech:
            speak("Ending Program")
            break
            pygame_thread.end()
            pygame.quit()
            os.system(clear)
        elif 'exit' in speech:
            speak("Exiting Boss")
            break
            pygame_thread.end()
            pygame.quit()
            os.system(clear)
        elif 'shut down' in speech:
            speak("Shutting Down Boss")
            break
            pygame_thread.end()
            pygame.quit()
            os.system(clear)
        elif 'shutdown' in speech:
            speak("Shutting Down Boss")
            break
            pygame_thread.end()
            pygame.quit()
            os.system(clear)
        elif 'goodbye' in speech:
            speak("Goodbye Boss")
            break
            pygame_thread.end()
            pygame.quit()
            os.system(clear)


def Jmain():
     porcupine = None
     pa = None
     audio_stream = None

     try:
        sensitivity = 1.0
        porcupine = pvporcupine.create(
            access_key='n0pfK6Juy8ZHWuczObvsz2Uj8F5xOiRgREwoAbWJgzajcqWfCdpIPw==',
            keyword_paths=[CUSTOM_KEYWORD_PATH],
            sensitivities=[sensitivity]
        )
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
               os.system('clear')
               print(" ")
               # Start the Pygame animation in a separate thread
               pygame_thread = threading.Thread(target=pygame_animation)
               pygame_thread.start()
               print("Welcome Back Boss, what can i Help you with today")
               speak("Welcome Back Boss, what can i Help you with today")
               print(" ")
               ConversationFlow()
               time.sleep(1)
               print("Don't forget, i am here if you need anything, " + USER)
               speak("Don't forget, i am here if you need anything, " + USER)
               print(" ")

     finally:
            if porcupine is not None:
                porcupine.delete()
            if audio_stream is not None:
                audio_stream.close()
            if pa is not None:
                pa.terminate()

Jmain()