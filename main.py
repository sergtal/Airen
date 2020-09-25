# Голосовой ассистент AIREN 1.1.0 BETA
import pyaudio
import speech_recognition as sr
import sys
import pyttsx3
from fuzzywuzzy import fuzz
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import re

opts = {
    "alias": ('айрен','арин','иран','айра','асиссистент','iron'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси'),
    "searchnet": ('найди','поиск','поищи'),
    "cmds": {
        "hi1": ('привет','добрый день','доброе утро','добрый вечер','здравствуй','здарова','hello','hi','good morning','good evening','приветики','приветствую'),
        'startStopwatch': ('запусти секундомер', "включи секундомер", "засеки время"),
        'stopStopwatch': ('останови секундомер', "выключи секундомер", "останови"),
        "calc": ('прибавить','умножить','разделить','степень','вычесть','поделить','х','+','-','/'),
        "shutdown": ('выключи', 'выключить', 'отключение', 'отключи', 'выключи компьютер'),
        "conv": ("валюта", "конвертер","доллар",'руб','евро'),
        "internet": ("открой", "вк", "гугл", "сайт", 'вконтакте', "ютуб"),
        "translator": ("переводчик","translate"),
        "deals": ("дела","делишки", 'как сам', 'как дела'),
        "ctime": ('текущее время','сколько времени','сейчас времени','который час','время','какое сейчас время'),
        "radio": ('включи музыку','воспроизведи радио','включи радио'),
        "stupid1": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты',"шутка","прикол"),
        "searchnet": ('найди','поиск','поищи')
    }
}

def speak(what):
    print( what )
    speak_engine = pyttsx3.init()
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()
   
r = sr.Recognizer()   
m = sr.Microphone(device_index = 1)
count = 0

def callibrating():  
    with m as source:   
        print("Please wait. Calibrating microphone...")   
        # listen for 5 seconds and calculate the ambient noise energy level   
        r.adjust_for_ambient_noise(source, duration=5)
        r.dynamic_energy_threshold = True  
        print("Say something!")
callibrating()

print("My commands: Привет/Время/Найди(что-то)/Включи радио/Стоп")

def search_google(cmd):
    browser = webdriver.Chrome("C:/Users/sergey/Downloads/chromedriver.exe")
    browser.get('http://www.google.com/')
    search = browser.find_element_by_name('q')
    search.send_keys(cmd)
    search.send_keys(Keys.RETURN)
    time.sleep(10) # Let the user actually see something!
    browser.quit()

def callback(recognizer, audio):
    try:
        global voice
        voice = r.recognize_google(audio, language = "ru-RU").lower()
        speak("Вы сказали: " + voice)
        print("[log] speech was: " + voice)
        if voice.startswith(opts["alias"]):
            # обращаются к AIREN
            cmd = voice
            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip() 
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip() 
            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])
    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError:
        print("[log] Неизвестная ошибка, проверьте интернет!")

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC

def execute_cmd(cmd):
    print(voice)
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))  
    elif cmd == 'hi1':
        # приветствие
        speak("Привет!")
    elif cmd == 'radio':
        # воспроизвести радио
        speak("hahah")
    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")
    elif cmd == 'searchnet':
        # поиск в chrome
        for x in opts['alias']:
            cmd = voice.replace(x, '')
        for x in opts['searchnet']:
            cmd = cmd.replace(x, '')
        search_google(cmd)  
    elif cmd == 'shutdown':
        # остановка
        speak("Останавливаю")
        sys.exit()
    else:
        print('Команда не распознана, повторите!')

with m as source:
    audio=r.listen(source)

stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some unrelated computations for 5 seconds
while True: time.sleep(0.1)