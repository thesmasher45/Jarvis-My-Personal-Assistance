import pyttsx3
import speech_recognition as sr
import datetime
import MyAlarm
import webbrowser
import pyautogui
from Functions.online_ops import find_my_ip, get_latest_news_, play_on_youtube, search_on_google, search_on_wikipedia, send_whatsApp_message, sendEmail
from Functions.os_ops import open_camera, open_cmd, open_notepad, open_vscode, play_music
import psutil
import os
import speedtest
from pywikihow import search_wikihow
import requests
from bs4 import BeautifulSoup
from random import choice
from utils import opening_text
import cv2
import numpy as np
import pyautogui as p


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Jarvis sir. Please tell me how may I help you")


def takeCommand():
    # It take microphone input from the user and return string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        speak(choice(opening_text))

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query


def TaskExecution():
    p.press('esc')
    speak("Verification successful")
    speak("Welcome Tejas sir")

    wishMe()
    while True:
        query = takeCommand().lower()
        # logic for executing tasks base on query
        if 'wikipedia' in query:
            speak("what do you want to search on Wikipedia, sir?")
            query = takeCommand()
            results = search_on_wikipedia(query)
            speak("Accroding to Wikipedia, ")
            speak("For your convenience, I am printing it on the screen sir.")
            print(results)
            speak(results)


        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            speak("What do you want to search on youtube, sir?")
            video = takeCommand()
            play_on_youtube(video)


        elif 'volume up' in query:
            pyautogui.press("volumeup")

        elif 'volume down' in query:
            pyautogui.press("volumedown")

        elif 'volume mute' in query or 'mute' in query:
            pyautogui.press("volumemute")


        elif 'open notepad' in query:
            open_notepad()

        elif 'close notepad' in query:
            speak("Okay sir, I am closing notepad.")
            os.system("taskkill /f /im notepad.exe")


        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()


        elif 'open camera' in query:
            open_camera()


        elif 'open google' in query:
            webbrowser.open("google.com")
            speak("What do you want to search on google, sir?")
            query = takeCommand()
            search_on_google(query)


        elif 'play music' in query:
            play_music()


        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, The time is {strTime}")


        elif 'set alarm' in query:
            speak("Sir please tell me the time to set alarm.")
            tt = takeCommand()
            tt = tt.replace("set alarm to ", "")
            tt = tt.replace(".", "")
            tt = tt.upper()
            MyAlarm.alarm(tt)


        elif 'open code' in query:
            open_vscode()

        elif 'close code' in query:
            speak("Okay sir, I am closing vscode.")
            os.system("taskkill /f /im code.exe")


        elif 'how much power left' in query or 'how much power we have' in query or 'battery' in query:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak(f"Sir our system have {percentage} percent battery")
            if percentage > 80:
                speak("Sir we have enough power to continue our work..")
            elif percentage >= 40 and percentage <= 80:
                speak(
                    "sir we should connect our system to charging point to charge out battery..")
            elif percentage <= 15 and percentage <= 30:
                speak(
                    "Sir we don't have enough power to work, please connect to charging point..")
            elif percentage <= 15:
                speak(
                    "Sir we have very lower power, please connect to charging point the system will shut down very soon..")


        elif 'hide all files' in query or 'hide this folder' in query or 'visible for everyone' in query:
            speak(
                "Sir, please tell me you want to hide this folder or make it visible for everyone..")
            condition = takeCommand()
            if 'hide' in condition:
                os.system("attrib +h /s /d")
                speak("Sir, all the files in this folder are now hidden.")

            elif 'visible' in condition:
                os.system("attrib -h /s /d")
                speak("Sir, all the files in this folder are now visible to everyone. I wish you are taking this decision in your own peace.")

            elif 'leave it' in condition or 'leave for now' in condition:
                speak("Ok sir.")


        elif 'internet speed' in query:
            st = speedtest.Speedtest()
            dl = st.download()
            up = st.upload()
            speak(
                f"Sir we have {dl} bit per second downloading speed and {up} bit per second uploading speed.")


        elif "send message" in query:
            speak("Please mention recipient's whatsapp number sir..")
            number = input("Enter the number: ")
            speak("What message would you like to give, sir?")
            message = takeCommand()
            send_whatsApp_message(number, message)
            speak("Message has been sent!")


        elif 'send email' in query:
            speak("Please mention recipient's email address sir..")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject sir?")
            subject = takeCommand().capitalize()
            speak("What message would you like to give, sir?")
            message = takeCommand()
            if sendEmail(receiver_address, subject, message):
                speak("Email has been sent!")
            else:
                speak("Sorry Sir. I am not able to send this mail")


        elif 'show latest news' in query:
            speak(f"I am reading out the latest news headlines, sir")
            speak(get_latest_news_())
            speak("For your convenience, I am printing it on the screen sir.")
            print(*get_latest_news_(), sep='\n')


        elif 'weather' in query:
            search = "weather in bharane"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp = data.find("div", class_="BNeawe").text
            speak(f"Current {search} is {temp}")
            print(temp)


        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            print(f'Your IP Address is {ip_address}')


        elif 'Where I am' in query or 'Where we are' in query:
            speak("Wait sir, let me check..")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                url = 'https://app.geojs.io/s/117.99.247.201'+ipAdd+'.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()

                city = geo_data['city']
                country = geo_data['country']
                speak(f"Sir I am not sure, but I think we are in {city} city of {country} country")
            except Exception as e:
                speak("Sorry sir, Due to network issue I am not able to find where we are.")
                pass


        elif 'activate how to do mod' in query:
            speak("How to do mode is activated sir.")
            while True:
                speak("Please tell me what you want to know sir")
                how = takeCommand()
                try:
                    if "exit" in how or "close" in how:
                        speak("Ok sir, how to do mode is closed.")
                        break
                    else:
                        max_results = 1
                        how_to = search_wikihow(how, max_results)
                        assert len(how_to) == 1
                        how_to[0].print()
                        speak(how_to[0].summary)
                except Exception as e:
                    speak("Sorry sir, I am not able to find this..")


        elif 'shut down the system' in query:
            os.system("shutdown /s /t 5")

        elif 'restart the system' in query:
            os.system("shutdown /r /t 5")

        elif 'jarvis quit' in query:
            speak("Thank You Sir. Have a good day..")
            exit()


if __name__ == "__main__":

    recognizer = cv2.face.LBPHFaceRecognizer_create()  # Local Binary Patterns Histograms
    recognizer.read('Trainer/Trainer.yml')  # Load trained model
    cascadePath = "haarcascade_frontalface_default.xml"  # Initializing haar cascade for object detection approch
    
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX  # Denotes the font type

    id = 2  # Number of persons you want to recognize

    names = ['', 'Teju']  # Names, leave first empty because counter start from 0


    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW to remove warning
    cam.set(3, 640)   # Set video FrameWidth
    cam.set(4, 480)   # Set video FrameHeight

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)


    while True:

        ret, img = cam.read()  # Read the frame using the above created object
        converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # The functions converts an input image from one color space to another

        faces = faceCascade.detectMultiScale(
            converted_image,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for(x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Use to draw a rectangle on any image
            id, accuracy = recognizer.predict(converted_image[y:y+h, x:x+w])  # To predict on every single image

            # Check if accuracy is less than 100 --> "0" is perfect match
            if (accuracy < 100):
                id = names[id]
                accuracy = "  {0}%".format(round(100 - accuracy))
                TaskExecution()

            else:
                id = "unknown"
                accuracy = "  {0}%".format(round(100 - accuracy))
                speak("User authentication is failed..")
                break
            
            cv2.putText(img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(accuracy), (x+5, y+h-5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break


# Do a bit of cleanup
print("Thanks for using this program, have a good day.")
cam.release()
cv2.destroyAllWindows()
