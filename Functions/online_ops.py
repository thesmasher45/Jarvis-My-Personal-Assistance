from ipaddress import ip_address
import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config


EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")
NEWS_API_KEY = config("NEWS_API_KEY")


def find_my_ip():
    ip_address = requests.get('https://api.ipify.org').text
    return ip_address

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def play_on_youtube(video):
    kit.playonyt(video)

def search_on_google(query):
    kit.search(query)

def send_whatsApp_message(number, message):
    kit.sendwhatmsg_instantly(f"+91{number}", message)

def sendEmail(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(email)
        server.close()
        return True
    except Exception as e:
        print(e)
        return False

def get_latest_news_():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]

