import time
from datetime import datetime
import pyttsx3

#initialize the pyttsx3 engine
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
time.sleep(2)


#Greeting
def WishMe():
        hour = datetime.datetime.now().hour
        if hour >= 3 and hour < 12:
            engine.say('Good morning boss')
        if hour >= 12 and hour < 18:
            engine.say('Good afternoon boss')
        if hour >= 18 and hour < 21:
            engine.say('Good evening boss')
        if hour >= 21 and hour < 24:
            engine.say("Go to bed boss it's to late")
        if hour >= 0 and hour < 3:
            engine.say("boss it's too late")
            engine.say("how can i help you")
WishMe()


time.sleep(2)