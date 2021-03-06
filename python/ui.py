#!/usr/bin/env python

import PySimpleGUI as ui
import configparser
import subprocess
import sys
import os
from threading import Thread
from queue import Queue, Empty
import signal

# Utils
process = None
ON_POSIX = 'posix' in sys.builtin_module_names
q = Queue()

def enqueue_output(out, queue):
    for line in iter(out.readline, ''):
        queue.put(line)
    out.close()

# Read config file
parser = configparser.ConfigParser()
parser.read('/home/pi/robokerho/config')

# Build UI
layout = [[ui.Text("Robohemian: "+parser.get('env', 'name'), font="arial 16 bold")],
          [ui.Button("CONFIG", button_color="orange"), ui.Button("RUN", button_color="green"), ui.Button("STOP", button_color="brown"), ui.Button("SHUTDOWN")],
          [ui.Multiline(reroute_stdout=True, reroute_stderr=True, auto_refresh=True, autoscroll=True, expand_x=True, expand_y=True, no_scrollbar=True)]]
window = ui.Window("Robohemian: "+parser.get('env', 'name'), layout, size=(420, 320), default_button_element_size=(11, 4), auto_size_buttons=False, resizable=True)

# Helpers
def start(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1, close_fds=ON_POSIX)
    t = Thread(target=enqueue_output, args=(process.stdout, q))
    t.daemon = True
    t.start()

# Main loop
while True:
    event, values = window.read(10)
    window.maximize()

    if event == "CONFIG":
        start(['killall', 'python3'])
        if not process:
            start(['python3', '/home/pi/robokerho/python/config.py'])

    if event == "RUN":
        start(['killall', 'python3'])
        if not process:
            if (parser.get('env', 'robo') == 'veke'):
                start(['python3', '/home/pi/robokerho/python/veke_2.py'])
            else:
                start(['python3', '/home/pi/robokerho/python/torch2.py'])

    if event == "STOP":        
        start(['killall', 'python3'])
        if process:
            process.stdout.close()
            process.send_signal(signal.SIGTERM)        

    if event == "SHUTDOWN":
        start(['sudo', 'shutdown', 'now'])

    if event == ui.WIN_CLOSED:
        start(['killall', 'python3'])
        if process:
            process.stdout.close()
            process.send_signal(signal.SIGTERM)
        break

    try: line = q.get_nowait()
    except Empty:
        continue
    else: print(line)

window.close()
