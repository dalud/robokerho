from wlanIF import Wlan
from arduinoIF import Arduino
from random import random
from time import sleep
import sys
import signal
import os
import subprocess
from threading import Thread


# Helpers
flush = sys.stdout.flush

# Init Wlan
wlan = Wlan()
flush()

# Init Arduino
arduino = Arduino()
arduino.connect()
flush()

def signal_term_handler(signal, frame):
    print("SIGTERM")
    wlan.stop()
    resetMotors()
    sys.exit()
    stop()
    start(['killall', 'python3'])

signal.signal(signal.SIGTERM, signal_term_handler)
#signal.signal(signal.SIGINT, signal_term_handler)

def speak(amp):
    #print("MEikä puhhuu" + amp)
    arduino.write('mm' + amp) # Kädet integrated into mm ?
    arduino.write('ex' + amp)
    # Kaulat
    arduino.write('kv' + amp)
    arduino.write('ko' + amp)

    # Blink
    if(random() < .2):
        arduino.write('b')
        sleep(.3)
    #arduino.write('')

def resetMotors():
    #arduino.write('kv' + str(90))
    #arduino.write('ko' + str(90))
    #arduino.write('mm' + str(0))
    arduino.write('ex' + str(500))
    arduino.write('z')
    arduino.write('')
    flush()
resetMotors()

def start(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1, close_fds=ON_POSIX)
    t = Thread(target=enqueue_output, args=(process.stdout, q))
    t.daemon = True
    t.start()

def stop():
    print("User exit")
    flush()     
    resetMotors()    
    sys.exit()
    os.kill(os.getpid(), signal.SIGINT)
    os.kill(os.getpid(), signal.SIGTERM)
    start(['killall', 'python3'])
    flush()

# Main loop
#while(True):    
    #flush()
    #try:
        #hear = wlan.listen()
        #if("veke" in hear[0].decode()):
            #print("Nyt meikä")
            #speak(hear[0].decode().split(':')[1])
            #flush()
        #else:
            #resetMotors()
while(True):
    flush()
    try:
        wlan.broadcast('snoozing')

        if not wlan.listen():
            flush()
        else:
            hear = wlan.listen()
            if("veke" in hear[0].decode()):
                print("Nyt meikä")
                speak(hear[0].decode().split(':')[1])
                flush()
            else:
                resetMotors()

    except KeyboardInterrupt:
        print("Keyboard interrupt")
        resetMotors()
        wlan.stop()
        stop()
        start(['killall', 'python3'])

    except:
        resetMotors()
