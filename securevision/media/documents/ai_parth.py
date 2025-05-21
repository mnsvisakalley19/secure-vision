import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("welcome to vidya, how can I assist you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening.....")
        r.pause_threshold = 0.8  # reduced for quicker response
        r.dynamic_energy_threshold = True
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return "none"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        speak("Sorry, I couldn't connect to the speech recognition service.")
        return "none"
    
    return query.lower()

# Additional functions for time, opening websites, etc.
def tellTime():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {strTime}")

def openWebsite(site_name):
    websites = {
        'youtube': 'youtube.com',
        'google': 'google.com',
        'github': 'github.com',
    }
    if site_name in websites:
        webbrowser.open(websites[site_name])
        speak(f"Opening {site_name}")
    else:
        speak("Sorry, I don't know this website.")

# Main function
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if query == "none":
            continue
        
        # Wikipedia Search
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except wikipedia.DisambiguationError as e:
                speak(f"Can you be more specific? I found multiple topics: {str(e.options[:3])}")
            except Exception as e:
                speak("Sorry, I couldn't find any information on that topic.")

        # Open websites
        elif 'open youtube' in query or 'youtube' in query:
            openWebsite('youtube')

        elif 'open google' in query or 'google' in query:
            openWebsite('google')
        
        elif'open github' in query or 'github' in query:
            openWebsite('github')

        # Tell time
        elif 'time' in query or 'what time is it' in query:
            tellTime()


        elif 'start' in query:
            speak("i am vidhya , a virtual ai cyber detector agent, and i am helping you in every kind of task you gave me but i am specially designed to detect cyber problems")
        elif'detect the system' in query:
            speak(" vidhya detecting")
            speak("you are safe thank you")
        # Exit or stop the program
        elif 'exit' in query or 'stop' in query:
            speak("Goodbye! Have a nice day.")
            break

        # If no recognized command
        else:
            speak("I'm sorry, I don't understand that. Could you try saying it differently?")
