#!/usr/bin/env python3
from qrReader import *
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
displayCustomers = tk.StringVar()
totalCustomers = 0

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

    submitbutton = tk.Button(window, text = "Submit", command=lambda:subpatient(window))
    submitbutton.pack()

def createuserprof():
    window = tk.Toplevel()
    window.geometry('300x300')
    newlabel = tk.Label(window, text = "Verifying Status")
    newlabel.pack()

    userentry = tk.Label(window, text = "Enter your password")
    userpw = tk.Entry(window, textvariable=usrpw, show="*")
    userentry.pack()
    userpw.pack()

    submitbutton = tk.Button(window, text = "Submit", command=lambda:subcheck(window))
    submitbutton.pack()

def createbusiness():
    global totalCustomers
    window = tk.Toplevel()
    window.geometry('300x300')
    displayCustomers.set(str(totalCustomers))

    tk.Label(window, text = "Total Customers = ").grid(row=0,column=0)
    tk.Label(window, textvariable=displayCustomers).grid(row=1,column=0)

    tk.Label(window, text = "Reset Customer Counter").grid(row=2,column=0)
    tk.Button(window, text = "Reset", command=lambda:subreset()).grid(row=3,column=0)

    tk.Label(window, text = "Manual Increase Customer Counter").grid(row=4,column=0)
    tk.Label(window, text = "*only use for those who cannot get vaccinated*").grid(row=5,column=0)
    tk.Button(window, text = "Increment", command=lambda:subincrease()).grid(row=6,column=0)

    tk.Label(window, text = "Manual Decrease Customer Counter").grid(row=7,column=0)
    tk.Button(window, text = "Decrement", command=lambda:subdecrease()).grid(row=8,column=0)

def subreset():
    global totalCustomers
    totalCustomers = 0
    displayCustomers.set(str(totalCustomers))

def subincrease():
    global totalCustomers
    totalCustomers += 1
    displayCustomers.set(str(totalCustomers))

def subdecrease():
    global totalCustomers
    totalCustomers -= 1
    if totalCustomers < 0:
        totalCustomers = 1
    displayCustomers.set(str(totalCustomers))

def subpatient(window):
    doctor = usrnm.get()
    doctor2 = sha256(usrpw.get().encode()).hexdigest()
    patient = patnm.get()
    patient2 = sha256(patpw.get().encode()).hexdigest()
    patient = generate_qr(patient)
    data = {"user":doctor, "pass":doctor2, "new_user":patient, "new_pass":patient2}
    print(data)
    r = requests.post("http://127.0.0.1:8081/Update", json=data)
    if r.text == "Success":
        window.configure(bg="green")
    else:
        window.configure(bg="red")

def subcheck(window):
    global totalCustomers
    patient = read_qr()
    patient2 = sha256(usrpw.get().encode()).hexdigest()
    print(patient, patient2)
    r = requests.get("http://127.0.0.1:8081/Check", auth=(patient, patient2))
    if r.text == "Success":
        window.configure(bg="green")
        subincrease()
    else:
        window.configure(bg="red")

def businessAndUser():
    createbusiness()
    createuserprof()

if __name__ == '__main__':

    tk.Label(top, text="WELCOME TO THE VACCINE PASSPORT SYSTEM").grid(row=0,column=0)
    tk.Label(top, text="Are you a Medical Professional? ").grid(row=1,column=0)
    yesDrbutton = tk.Button(top, text="Yes", command=createmedprof).grid(row=1,column=1)
    tk.Button(top, text="No", command=createuserprof).grid(row=1, column=2)
    tk.Label(top, text="Are you a Business? ").grid(row=2,column=0)
    yesBusbutton = tk.Button(top, text="Yes", command=businessAndUser).grid(row=2,column=1)
    tk.Button(top, text="No", command=createuserprof).grid(row=2, column=2)
    top.mainloop()
