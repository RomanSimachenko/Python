import speech_recognition as sr
import pyttsx3


listener = sr.Recognizer()
engine = pyttsx3.init()

# engine.say("Hi, this is Tina speaking, virtual assistent of restaurant Mangare, to start off: "
#            "do you want to make a reservation in our restaurant?")
engine.say("Hello, Tina!")
engine.runAndWait()

with sr.Microphone() as source:
    print('listening...')
    voice = listener.listen(source)
    command = listener.recognize_google(voice)
    print(command)