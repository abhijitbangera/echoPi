import vlc
import urllib
from bs4 import BeautifulSoup
from pytube import YouTube
import re
import os
import ssl


ssl._create_default_https_context = ssl._create_unverified_context


class EchoPi:

    def __init__(self):
        self.is_alive = True
        self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
        self.my_song = vlc.MediaPlayer(self.desktop_path + os.sep+ "myfile.mp4")

    def download_video(self, url):
        print ('url is:', url)
        print ("Playing ",YouTube(url).title)
        yt=YouTube(url).streams.first().download(
            self.desktop_path, filename='myfile')
        print ('done')
        self.playAudio()

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

    def playAudio(self):
        self.my_song.play()
        while self.is_alive:
            self.stopAudio()

    def stopAudio(self):
        x=raw_input("Enter:")
        if x.lower() == "stop":
            print ("Stopping audio playback..")
            self.my_song.stop()
            self.is_alive = False
            return self.is_alive

obj=EchoPi()
obj.search_video('lungi dance')
