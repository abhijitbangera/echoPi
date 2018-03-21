import vlc
import urllib
from bs4 import BeautifulSoup
from pytube import YouTube
import re
import os
import ssl
import speech_recognition as sr
import pyttsx
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

    def get_answer(self, question):
        app_id = ''  # wolframalpha app ID
        print "question is:", question
        if question == "who are you" or question == "what is your name":
            answer = "I am Jarvis"
        else:
            try:
                client = wolframalpha.Client(app_id)
                res = client.query(question)
                print "res is:", res
                for pod in res.pods:
                    for sub in pod.subpods:
                        print "inside pods"
                        print(sub)
                print ('$$$$$$$$$$$$$$$$$$$$$$$')
                print(next(res.results).text)
                answer = next(res.results).text
            except Exception as e:
                print e
                answer = "Something went wrong. Lets try it again. Shall we?"
        engine = pyttsx.init()
        # engine.say('Sally sells seashells by the seashore.')
        engine.say(answer)
        # update_text(answer)
        engine.runAndWait()
        return

    def speech_reg(self):
        print 'sound reg.......'

        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)
            try:
                userinput = r.recognize_google(audio)
                print userinput
                userinput_split = userinput.split(" ")
                if userinput!="stop" and userinput_split[0]=="play":
                    y= userinput_split
                    z=y[1:]
                    p = threading.Thread(target=self.search_video, args=(" ".join(map(str, z)),))
                    # jobs.append(p)
                    p.start()

                elif userinput == "stop":
                    print ("Stopping audio playback..")
                    self.my_song.stop()
                    self.is_alive = False
                    return self.is_alive
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
        # print ('url is:', url)
        # print ("Playing ",YouTube(url).title)
        # song_title = YouTube(url).title
        # print "song title is:", song_title
        # engine = pyttsx.init()
        # # engine.say('Sally sells seashells by the seashore.')
        # engine.say("playing "+song_title)
        # engine.runAndWait()
        # yt=YouTube(url).streams.first().download(
        #     self.desktop_path, filename='myfile')
        myfile = self.desktop_path + os.sep + "myfile.mp4"
        os.remove(myfile) if os.path.exists(myfile) else None
        yt = YouTube(url).streams.filter(only_audio=True)
        yt.first().download(
            self.desktop_path, filename='myfile')
        print ('done')
        # self.playAudio()
        self.my_song.play()
        print ('done playing song')
        return


    def search_video(self, text):
        textToSearch = text
        query = urllib.quote_plus(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html,"lxml")
        mylist=[]
        for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
            y= 'https://www.youtube.com' + vid['href']
            mylist.append(y)
        print (mylist)
        if re.match(r'https://www.youtube.com/watch', mylist[0]):
            song_to_play = mylist[0]
        else:
            song_to_play =  mylist[1]
        self.download_video(song_to_play)
        return
    #
    # def playAudio(self):
    #     self.my_song.play()
    #     while self.is_alive:
    #         self.stopAudio()


    def stopAudio(self):

        userinput =raw_input("Enter:")
        if userinput.lower() == "stop":
            print ("Stopping audio playback..")
            self.my_song.stop()
            self.is_alive = False
            return self.is_alive


obj=EchoPi()
# obj.search_video('lungi dance')
obj.speech_reg()