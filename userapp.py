#!/usr/bin/env python3
from qrReader import *
import tkinter as tk
import requests
from flask_httpauth import HTTPBasicAuth
from hashlib import sha256
import sys

auth = HTTPBasicAuth()
top = tk.Tk()
usnm = tk.StringVar()
pw = tk.StringVar()
if len(sys.argv) < 2:
    URL = "127.0.0.1"
else:
    URL = sys.argv[1]


def EntryCheck():
    patient = sha256(usnm.get().encode()).hexdigest()
    patient2 = sha256(pw.get().encode()).hexdigest()
    r = requests.get("http://" + URL + "/Check")
    if r.text == "Success":
        createuserwindow()

def createuserprof():
    window = tk.Toplevel()
    window.geometry('300x300')
    newlabel = tk.Label(window, text = "Verifying Status")
    newlabel.pack()

    userentry = tk.Label(window, text = "Enter your password")
    userpw = tk.Entry(window, textvariable=usrpw, show="*")
    userentry.pack()
    userpw.pack()
    newscan = tk.Button(window, text="New Scan", command=lambda:newuserprofile(window))
    submitbutton = tk.Button(window, text = "Submit", command=lambda:subcheck(window))
    submitbutton.pack()
    newscan.pack()

def qrget():
    r = requests.get("http://" + URL + "/QRget/{}".format(username))
    generate_qr(r.text)
def hisget():
    r = requests.get("http://" + URL + "/HistoryGet/NULL/{}".format(username)) #<business>/<user>
    print(r.json)

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
