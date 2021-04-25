#!/usr/bin/env python3

import tkinter as tk
import requests
from flask_httpauth import HTTPBasicAuth
from hashlib import sha256

auth = HTTPBasicAuth()
top = tk.Tk()
usrnm = tk.StringVar()
usrpw = tk.StringVar()
patnm = tk.StringVar()
patpw = tk.StringVar()

def createmedprof():
    window = tk.Toplevel()
    window.geometry('300x300')
    newlabel = tk.Label(window, text = "Adding New User")

    userentry = tk.Label(window, text = "Enter Doctor username/password")
    username = tk.Entry(window, textvariable=usrnm)
    userpw = tk.Entry(window, textvariable=usrpw, show="*")
    newlabel.pack()
    userentry.pack()
    username.pack()
    userpw.pack()

    Vaccinated = tk.Label(window, text= "Enter New Patient")
    Vaccinated.pack()
    patname = tk.Entry(window, textvariable=patnm)
    patpass = tk.Entry(window, textvariable=patpw, show="*")
    patname.pack()
    patpass.pack()

    submitbutton = tk.Button(window, text = "Submit", command=subpatient)
    submitbutton.pack()

def createuserprof():
    window = tk.Toplevel()
    window.geometry('300x300')
    newlabel = tk.Label(window, text = "Verifying Status")
    newlabel.pack()

    userentry = tk.Label(window, text = "Enter your username/password")
    username = tk.Entry(window, textvariable=usrnm)
    userpw = tk.Entry(window, textvariable=usrpw, show="*")
    userentry.pack()
    username.pack()
    userpw.pack()

    submitbutton = tk.Button(window, text = "Submit", command=subcheck)
    submitbutton.pack()


def subpatient():
    doctor = usrnm.get()
    doctor2 = sha256(usrpw.get().encode()).hexdigest()
    patient = patnm.get()
    patient2 = sha256(patpw.get().encode()).hexdigest()
    data = {"user":doctor, "pass":doctor2, "new_user":patient, "new_pass":patient2}
    print(data)
    # requests.post("http://127.0.0.1:8081/Update", json=data)

def subcheck():
    patient = usrnm.get()
    patient2 = sha256(usrpw.get().encode()).hexdigest()
    print(patient, patient2)
    # requests.get("http://127.0.0.1:8081/Check", auth=(patient, patient2))

if __name__ == '__main__':

    tk.Label(top, text="WELCOME TO THE VACCINE PASSPORT SYSTEM").grid(row=0,column=0)
    tk.Label(top, text="Are You a Medical Professional? ").grid(row=1,column=0)
    yesbutton = tk.Button(top, text="Yes", command=createmedprof).grid(row=1,column=1)
    tk.Button(top, text="No", command=createuserprof).grid(row=1, column=2)
    top.mainloop()
