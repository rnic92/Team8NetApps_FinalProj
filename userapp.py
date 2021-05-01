#!/usr/bin/env python3
from qrReader import *
import tkinter as tk
import requests
from flask_httpauth import HTTPBasicAuth
from hashlib import sha256
import sys
from PIL import Image

patient = ''
patient2 = ''
auth = HTTPBasicAuth()
top = tk.Tk()
usnm = tk.StringVar()
pw = tk.StringVar()
if len(sys.argv) < 2:
    URL = "127.0.0.1"
else:
    URL = sys.argv[1]


def EntryCheck():
    global patient, patient2
    patient = sha256(usnm.get().encode()).hexdigest()
    patient2 = sha256(pw.get().encode()).hexdigest()
    r = requests.get("http://" + URL + "/Check", auth=(patient,patient2))
    if r.text == "Success":
        createuserwindow()

def createuserwindow():
    window = tk.Toplevel()
    window.geometry('300x300')
    newlabel = tk.Label(window, text = "Welcome!")
    newlabel.pack()
    qrcode = tk.Button(window, text="Generate QR", command=qrget)
    history = tk.Button(window, text = "Get History", command=hisget)
    qrcode.pack()
    history.pack()

def qrget():
    global patient, patient2
    r = requests.get("http://" + URL + "/QRGet/{}".format(patient), auth=(patient, patient2))
    print(r.text)
    generate_qr(r.text)
    displayqr()
def hisget():
    global patient, patient2
    print(patient)
    r = requests.get("http://" + URL + "/HistoryGet/NULL/{}".format(patient), auth=(patient, patient2)) #<business>/<user>
    print(r.text)

def displayqr():
    im = Image.open("testfile.png")
    im.show()


if __name__ == '__main__':
    print(URL)
    top.geometry("400x200")
    top.title("WELCOME TO THE VACCINE PASSPORT SYSTEM")
    userLabel = tk.Label(top,text="Enter your Username ").grid(row=1,column=0)
    userEntry = tk.Entry(top, textvariable=usnm).grid(row=1,column=1)
    pwLabel = tk.Label(top,text="Enter your Username ").grid(row=2,column=0)
    pwEntry = tk.Entry(top, textvariable=pw).grid(row=2,column=1)
    subButton = tk.Button(top, text="Submit",command=EntryCheck).grid(row=3,column=1)

    top.mainloop()
