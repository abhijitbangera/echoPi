import vlc
import urllib
from bs4 import BeautifulSoup
from pytube import YouTube
import re
import os
import ssl
import speech_recognition as sr
import pyttsx3
import threading
import subprocess
import multiprocessing
import wolframalpha

ssl._create_default_https_context = ssl._create_unverified_context


class EchoPi:

    def __init__(self):
        self.is_alive = True
        self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        self.my_song = vlc.MediaPlayer(self.desktop_path + os.sep+ "myfile.mp4")
        self.r = None
        self.speak("Hello Sir, how can I help you?")
    
    def speak(self, text):
        engine = pyttsx3.init()
        #engine.setProperty('voice', 'english+f1')
        engine.say(text)
        engine.runAndWait()

    def get_answer(self, question):
        app_id = ''  # Enter wolframalpha app ID here
        print ("question is:", question)
        text="answer to your question is"
        self.speak(text)
        if question == "who are you" or question == "what is your name": # a small dirty cheat to look cool :P
            answer = "I am Jarvis"
        else:
            try:
                client = wolframalpha.Client(app_id)
                res = client.query(question)
                print ("res is:", res)
                for pod in res.pods:
                    for sub in pod.subpods:
                        print(sub)
                answer = next(res.results).text
                print (answer)
            except Exception as e:
                print (e)
                answer = "Something went wrong. Lets try it again. Shall we?"
        self.speak(answer)
        return

    def speech_reg(self):
        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)
            try:
                userinput = r.recognize_google(audio)
                #userinput="jarvis what is capital of India?"
                print (userinput)
                userinput_split = userinput.split(" ")
                if userinput!="stop" and userinput_split[0]=="play":
                    y= userinput_split
                    z=y[1:]
                    p = threading.Thread(target=self.search_video, args=(" ".join(map(str, z)),))
                    p.start()
                elif userinput == "stop":
                    print ("Stopping audio playback..")
                    self.my_song.stop()
                    self.is_alive = False
                    text="Audio playback stopped"
                    self.speak(text)
                    #return self.is_alive
                elif userinput_split[0].lower() == "jarvis":
                    y = userinput_split
                    z = y[1:]
                    self.get_answer(" ".join(map(str, z)))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                userinput = "Google Speech Recognition could not understand audio"
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def download_video(self, url):
        myfile = self.desktop_path + os.sep + "myfile.mp4"
        os.remove(myfile) if os.path.exists(myfile) else None
        yt = YouTube(url).streams.filter(only_audio=True)
        yt.first().download(self.desktop_path, filename='myfile')
        print ('done')
        self.my_song.play()
        print ('done playing song')
        return

    def search_video(self, text):
        text="playing "+str(text)+"in few seconds"
        self.speak(text)
        textToSearch = text
        query = urllib.parse.quote_plus(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html,"lxml")
        mylist=[]
        for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
            y= 'https://www.youtube.com' + vid['href']
            mylist.append(y)
        #print (mylist)
        if re.match(r'https://www.youtube.com/watch', mylist[0]):
            song_to_play = mylist[0]
        else:
            song_to_play =  mylist[1]
        self.download_video(song_to_play)
        return


obj=EchoPi()
# obj.search_video('lungi dance')
obj.speech_reg()