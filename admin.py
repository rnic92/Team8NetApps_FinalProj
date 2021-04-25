import requests
from hashlib import sha256
typ = input("enter type [Doctor/Patient]: ")
name = input("enter name: ")
psw = sha256(input("enter pw").encode()).hexdigest()

data = {"user":name, "pass":psw}
r = requests.post(("http://127.0.0.1:8081/Admin/" + typ), json=data)
print(r.text)
