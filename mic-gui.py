import gtts
from pygame import mixer
from urllib import parse
from gtts import gTTS
import pygame, keyboard, requests, os
from tkinter import *
mixer.init(devicename="CABLE Input(VB-Audio Virtual Cable)")
def stop():
    """stop function"""
    mixer.music.stop()
    mixer.music.unload()
def play(music, vol=1):
    stop()
    """play music function"""
    try:
        mixer.music.load(music)
        mixer.music.set_volume(vol)
        mixer.music.play(0)
    except Exception as e:
        return print(e)
def down(url):
    """download tts"""
    try:
        r = requests.get(url)
        r.raise_for_status()
        if len(r.content) == 360:
            return 'sans'
        f = open("./voice.mp3", "wb")
        f.write(r.content)
        f.close()
        return 'voice.mp3'
    except:
        print('cant download the tts file')
        os.remove('./voice.mp3')
        return False
ii = 0
window = Tk()
window.title( 'tts!' )
window.resizable(False, False)
frame = Frame( window )
wowbox = Listbox( frame, width=40,height=30)
def tts(event):
    """speak tts"""
    stop()
    txt = entry.get()
    entry.delete(0, 'end')
    mi = down(f"https://tts-translate.kakao.com/newtone?message=%s"%parse.quote(txt))
    globals()["wowbox"].insert(ii, txt)
    globals()["ii"] += 1
    if mi:
        if mi != 'sans':
            return play(mi)
        tts = gTTS(text=txt, lang='ko', slow=False)
        if txt.startswith('`en '):
            tts = gTTS(text=txt[4:], lang='en', slow=False)
        tts.save('voice.mp3')
        return play('voice.mp3')
print('stop playing is F7')
scrollbar=Scrollbar(frame)
scrollbar.pack(side="right", fill="y")
listbox = Listbox( frame, width=40,height=30, yscrollcommand = scrollbar.set)
i = 0
files = list(map(lambda x:os.path.splitext(x)[0], os.listdir('./sounds/')))
if not len(files):
    listbox.insert( 1, 'None' )
else:
    for item in files:
        listbox.insert(i, files[i])
        i+=1
def select(self):
    globals()["value"]=scale.get()
    mixer.music.set_volume(globals()["value"] / 10000)
def callback(event):
    stop()
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        play('./sounds/' + data + '.mp3', globals()["value"] / 10000)
def callb(event):
    stop()
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        mi = down(f"https://tts-translate.kakao.com/newtone?message=%s"%parse.quote(data))
        if mi:
            return play(mi)
listbox.pack( side = LEFT )
wowbox.pack(side = RIGHT)
scrollbar["command"]=listbox.yview
listbox.bind("<<ListboxSelect>>", callback)
wowbox.bind("<<ListboxSelect>>", callb)
button = Button(window, width=30, command=stop, repeatdelay=100, repeatinterval=100, text="정지")
button.pack( side = BOTTOM)
entry=Entry(window,width=30)
entry.bind("<Return>", tts)
entry.pack( side = BOTTOM)
var=IntVar()
var.set(3000)
value = 3000
scale=Scale(window, variable=var, command=select, orient="horizontal", showvalue=True, tickinterval=2000, to=10000, length=300, label="음량 조절")
scale.pack(side = BOTTOM)
frame.pack( padx = 30, pady = 50 )
listbox.bind("<Return>", tts)
window.mainloop()
