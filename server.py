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
print("[Server 01] – Initialized Doctors MongoDB datastore")
clusterVaccinated = pymongo.MongoClient("mongodb+srv://joshs98:VirginiaTech98@cluster0.duako.mongodb.net/Vaccinated?retryWrites=true&w=majority")
dbVaccinated = clusterVaccinated["Vaccinated"]
collectionVaccinated = dbVaccinated["Vaccinated"]
print("[Server 02] – Initialized Vaccinated MongoDB datastore")
clusterBusiness = pymongo.MongoClient("mongodb+srv://joshs98:VirginiaTech98@cluster0.duako.mongodb.net/Business?retryWrites=true&w=majority")
dbBusiness = clusterBusiness["Business"]
collectionBusiness = dbBusiness["Business"]
print("[Server 03] – Initialized Business MongoDB datastore")

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(AuthUsername, AuthPassword):
    DocVacInfo = collectionVaccinated.find_one({"Username":AuthUsername})
    if DocVacInfo:
        if AuthPassword == DocVacInfo.get("Password"):
            return AuthUsername
    print("failed auth")
    return None

@app.route('/Check', methods=['GET'])
@auth.login_required
def Check():
    print("[Server 04] – Varified Patient Information")
    return "Success"

@app.route('/HistoryPost', methods=['POST'])
@auth.login_required
def HistoryPost():
    data = request.get_json(force=True)
    BID = data['BID']
    user = data['user']
    timeEntered = time.ctime(time.time())
    postBusiness = {"BID": BID, "User": user,  "Time": timeEntered}
    collectionBusiness.insert_one(postBusiness)
    print("[Server 06] – Business Added Access Information")
    return "Success"

@app.route('/HistoryGet/<BID>/<user>', methods=['GET'])
@auth.login_required
def HistoryGet(BID,user):
    if user == 'NULL' and BID != 'NULL':
        BusinessUserInfo = dict(collectionBusiness.find({"User": user}))
    elif user != 'NULL' and BID == 'NULL':
        BusinessUserInfo = dict(collectionBusiness.find({"BID": BID}))
    elif user != 'NULL' and BID != 'NULL':
        BusinessUserInfo = dict(collectionBusiness.find({"BID": BID},{"User": user}))
    else:
        return "Error: Not enough information given"
    print("[Server 07] – Business History Accessed Information:")
    print(BusinessUserInfo)
    return BusinessUserInfo

@app.route('/QRGet/<user>', methods=['GET'])
@auth.login_required
def QRGet(user):
    return user

@app.route('/Update', methods=['POST'])
def Update():
    print("Made it here")
    data = request.get_json(force=True)
    DrUser = data['user']
    DrPass = data['pass']
    new_user = data['new_user']
    new_pass = data['new_pass']
    DocDrInfo = collectionDr.find_one({"Username":DrUser})
    if DrPass == DocDrInfo.get("Password"):
        ticks = time.time()
        TimeOfVaccination = str(ticks)
        postVaccinated = {"Username": new_user, "Password": new_pass, "Time": TimeOfVaccination}
        collectionVaccinated.insert_one(postVaccinated)
        print("[Server 05] – Doctor Added Patient Information")
        return "Success"
    return "Failure"

"""
@app.route('/Admin/<EntryType>', methods=['POST'])
def Admin(EntryType):
    data = request.get_json(force=True)
    AdUser = data['user']
    AdPass = data['pass']
    if EntryType == "Doctor":
        postDoctor = {"Username": AdUser, "Password": AdPass}
        collectionDr.insert_one(postDoctor)
        return "Success"
    elif EntryType == "Patient":
        ticks = time.time()
        TimeOfVaccination = str(ticks)
        postVaccinated = {"Username": AdUser, "Password": AdPass, "Time": TimeOfVaccination}
        collectionVaccinated.insert_one(postVaccinated)
        return "Success"
    return "Failure"
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)