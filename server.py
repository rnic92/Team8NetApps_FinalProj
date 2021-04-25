from flask import *
from flask_httpauth import HTTPBasicAuth
import requests, json
import sys
import time
import pymongo
from hashlib import sha256

clusterDr = pymongo.MongoClient("mongodb+srv://joshs98:VirginiaTech98@cluster0.duako.mongodb.net/Doctors?retryWrites=true&w=majority")
dbDr = clusterDr["Doctors"]
collectionDr = dbDr["Doctors"]
print("[Server 01] –Initialized Doctors MongoDB datastore")
clusterVaccinated = pymongo.MongoClient("mongodb+srv://joshs98:VirginiaTech98@cluster0.duako.mongodb.net/Vaccinated?retryWrites=true&w=majority")
dbVaccinated = clusterVaccinated["Vaccinated"]
collectionVaccinated = dbVaccinated["Vaccinated"]
print("[Server 02] –Initialized Vaccinated MongoDB datastore")

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(AuthUsername, AuthPassword):
    DocVacInfo = collectionVaccinated.find({"Username":AuthUsername})
    if sha256(AuthPassword.encode()) == DocVacInfo.get("Password"):
        return AuthUsername
    print("failed auth")
    return None

@app.route('/Check', methods=['GET'])
@auth.login_required
def Check():
    return "Success"

@app.route('/Update', methods=['POST'])
def Update():
    data = request.get_json(force=True)
    DrUser = data['user']
    DrPass = data['pass']
    new_user = data['new_user']
    new_pass = data['new_pass']
    DocDrInfo = collectionDr.find({"Username":DrUser})
    if sha256(DrPass.encode()) == DocDrInfo.get("Password"):
        ticks = time.time()
        TimeOfVaccination = str(ticks)
        postVaccinated = {"Username": new_user, "Password": new_pass, "Time": TimeOfVaccination}
        collectionVaccinated.insert_one(postVaccinated)
        return "Success"
    return "Failure"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081)