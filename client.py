#!/usr/bin/env python3
from qrReader import *
import tkinter as tk
import requests
from flask_httpauth import HTTPBasicAuth
from hashlib import sha256
import sys

auth = HTTPBasicAuth()
top = tk.Tk()
usrnm = tk.StringVar()
usrpw = tk.StringVar()
patnm = tk.StringVar()
patpw = tk.StringVar()
newMaxCustomers = tk.StringVar()
displayCustomers = tk.StringVar()
totalCustomers = 0
displayMaximum = tk.StringVar()
bids = tk.StringVar()
bid = 'Hokie House'
maximumCustomers = 100
if len(sys.argv) < 2:
    URL = "127.0.0.1:8081"
else:
    URL = sys.argv[1]

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
    newscan = tk.Button(window, text="New Scan", command=lambda:newuserprofile(window))
    submitbutton = tk.Button(window, text = "Submit", command=lambda:subcheck(window))
    submitbutton.pack()
    newscan.pack()


def newuserprofile(window):
    window.destroy()
    usrnm.set("")
    usrpw.set("")
    patnm.set("")
    patpw.set("")
    createuserprof()

def createbusiness():
    global totalCustomers, maximumCustomers, bid
    window = tk.Toplevel()
    window.geometry('500x250')
    displayCustomers.set(str(totalCustomers))
    displayMaximum.set(str(maximumCustomers))
    tk.Label(window, text = "Total Customers = ").grid(row=0,column=0)
    tk.Label(window, textvariable=displayCustomers).grid(row=1,column=0)

    tk.Label(window, text = "Maximum Allowable Customers = ").grid(row=0,column=1)
    tk.Label(window, textvariable=displayMaximum).grid(row=1,column=1)

    tk.Label(window, text = "Reset Customer Counter").grid(row=2,column=0)
    tk.Button(window, text = "Reset", command=lambda:subreset()).grid(row=3,column=0)

    tk.Label(window, text = "Manual Increase Customer Counter").grid(row=4,column=0)
    tk.Label(window, text = "*only use for those who cannot get vaccinated*").grid(row=5,column=0)
    tk.Button(window, text = "Increment", command=lambda:subincrease()).grid(row=6,column=0)

    tk.Label(window, text = "Manual Decrease Customer Counter").grid(row=4,column=1)
    tk.Label(window, text="*track when people leave to update counter*").grid(row=5, column=1)
    tk.Button(window, text = "Decrement", command=lambda:subdecrease()).grid(row=6,column=1)

    tk.Label(window, text = "Adjust Maximum Number of Customers: ").grid(row=7,column=0)
    tk.Entry(window, textvariable=newMaxCustomers).grid(row=8, column=0)
    tk.Button(window, text="Submit", command=setmax).grid(row=8,column=1)

    tk.Label(window, text="BID: {}".format(bid)).grid(row=9, column=0)
    tk.Entry(window, textvariable=bids).grid(row=9,column=1)
    tk.Button(window, text="Submit", command=setbid).grid(row=9,column=2)
    tk.Label(window, )

def setbid():
    global bid
    bid = bids.get()
def setmax():
    global maximumCustomers
    maximumCustomers = int(newMaxCustomers.get())
    displayMaximum.set(newMaxCustomers.get())

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
        totalCustomers = 0
    displayCustomers.set(str(totalCustomers))

def subpatient(window):

    doctor = usrnm.get()
    doctor2 = sha256(usrpw.get().encode()).hexdigest()
    patient = sha256(patnm.get().encode()).hexdigest()
    patient2 = sha256(patpw.get().encode()).hexdigest()
    patient = generate_qr(patient)
    data = {"user":doctor, "pass":doctor2, "new_user":patient, "new_pass":patient2}
    r = requests.post("http://" + URL + "/Update", json=data)
    if r.text == "Success":
        window.configure(bg="green")
    else:
        window.configure(bg="red")

def subcheck(window):
    global totalCustomers, maximumCustomers
    patient = read_qr()
    patient2 = sha256(usrpw.get().encode()).hexdigest()
    data = {"user": patient, "BID": bid}
    r = requests.get("http://" + URL + "/Check", auth=(patient, patient2))
    if r.text == "Success" and totalCustomers < maximumCustomers:
        nr = requests.post("http://" + URL + "/HistoryPost", auth=(patient, patient2), json=data)
        window.configure(bg="green")
        subincrease()
    elif r.text == "Success" and totalCustomers >= maximumCustomers:
        window.configure(bg="yellow")
        warningLabel = tk.Label(window,text="WARNING: MAXIMUM CAPACITY")
        warningLabel.pack()
    else:
        window.configure(bg="red")


if __name__ == '__main__':
    top.geometry("400x200")
    tk.Label(text="                   \n                  ").grid(row=5,column=1)
    tk.Label(text="                   \n                  ").grid(row=6,column=1)
    top.title("WELCOME TO THE VACCINE PASSPORT SYSTEM")
    entrybutton = tk.Button(top, text="Scan for entry", command=createuserprof, bg="#54FA9B").grid(row=0,column=0)
    yesDrbutton = tk.Button(top, text="Medical", command=createmedprof).grid(row=7,column=3)
    yesBusbutton = tk.Button(top, text="Settings", command=createbusiness).grid(row=7,column=4)
    top.mainloop()
