from socket import *

# Listen
def listen():
    ear = socket(AF_INET, SOCK_DGRAM)
    ear.bind(('', 12345))
    ear.settimeout(1)
    try:
        data = ear.recvfrom(1024)    
        if data: print('I hear:', data[0].decode())
    except: print("I hear nothing...")

# Speak
def speak():
    print('I am speaking')
    mouth = socket(AF_INET, SOCK_DGRAM)
    mouth.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    mouth.sendto(b'tok',('255.255.255.255',12345))

while True:
    listen()
    #speak()
