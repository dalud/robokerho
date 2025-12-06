#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wlanIF import Wlan
import os
from time import sleep
import sys
import signal
from tkinter import *
from subprocess import Popen, PIPE
import signal

wlan = Wlan()
#dir = '/home/pi/robokerho/samples/transcripts/'
dir = 'C:/robokerho/samples/transcripts/kiina/'
texts = os.listdir(dir)
print(texts)
root = Tk()
root.configure(bg="black", cursor="none")
root.attributes('-fullscreen', True)
text = Text(
    root,
    bg="black",
    fg="white",
    border=-10,
    padx=(root.winfo_screenwidth()/10),
    font=("Piboto", int(root.winfo_screenwidth()/31)),
    wrap=WORD,
    cursor="none"
)
text.tag_configure("center", justify='center')
text.tag_add("center", "1.0", "end")
text.pack(
    expand=True,
    fill='both',
    pady=(root.winfo_screenheight()/3+42, 0), #root.winfo_screenheight()/4),
)

def check():
    print("Checking...")
    root.after(50, check)

# TODO: resolve interrupt for Tk.root()

def update():
    text.update_idletasks()
    text.see("1.0")

def getSearchString():
    hear = wlan.listen()
    if hear:
        searchString = "not found"
        data = hear[0].decode().split(':')
        if 'veke' in data:
            searchString = data[3].replace('wav', 'txt')
        else:
            searchString = data[1].replace('wav', 'txt')
        print(searchString)
        return searchString

previous = ""
#debug = "Mitä jos onkin paljon tekstiä? Esimerkiksi vaikka 4 riviä, niin mistä se alkaa? Ja mistä tietää mahtuuko se näytölle? Ja kuinka paljon laitetaan paddingiä etc. mihinki laitaan? Onko olemassa vielä viideskin rivi siis?"

def quit(event):
    print(event)
    root.destroy()
    sys.exit(0)
    
def main(previous):
    while True:
        try:
            searchString = getSearchString()
            if searchString in texts and searchString != previous:
                file = open(dir+searchString, 'r', encoding='utf-8')
                lines = file.readlines()
                while lines:
                        hear = wlan.listen()
                        if hear:
                            time = int(hear[0].decode().split(':')[2])
                            comp = int(lines[0].split(':')[0])
                                    
                            if time >= comp:
                                sleep(1) # set desired offset
                                line = lines.pop(0)
                                text.delete("1.0", END)
                                update()
                                text.insert("1.0", line.split(':')[1], "center")
                                #text.insert("1.0", debug, "center")
                                update()
                                if line.split(':')[1] == '':
                                    text.delete("1.0", END)
                                    update()
                                    break
                        previous = searchString
        except KeyboardInterrupt as intr:
            quit(intr)
        
root.bind('<Control-c>', quit)
root.update_idletasks()
root.after(100, main(previous))
root.mainloop()
