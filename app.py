from email import message
from sqlite3 import Timestamp
from time import time
from urllib import response
from flask import Flask,request
from flask_cors import CORS, cross_origin
from flask import Flask

from main import encption, decryption


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


userarr = []  ##arrays of users
blockchain = [] 

cid  = []

def createUser(name, uid, pwd, type):
    d = {
        "name":name,
        "uid" : uid,
        "pwd":pwd,
        "type":type # 1 - voter 2 - candidate 3 - election admin
    }
    userarr.append(d)
    return True


ind = 0
def createBlock ( CID , UID, EID ):
    response = {

        "index": ind+1,
        "message" : "Thank you for voting. Your response has has been been saved successfully." ,

        "votes" : [{
            "CID" : CID,
            "UID" : UID,
            "EID" : EID
        }]

    }
    blockchain.append(response)
    return blockchain



@app.route('/', methods=["POST"])

def index():
    data= request.get_json()
    flag = createUser(data["name"], data["uid"] ,data["pwd"], data["type"])

    if flag:    
        return {

            "msg":"User added successfully.",
            "status":201,
        }
    else:    
        return {

            "msg":"Bad Request",
            "status":400,
        }

@app.route('/cast', methods=["POST"])

def castvote():
    data= request.get_json()
    response = createBlock(encption(data["CID"]), data["UID"], data["EID"]) ## encrypting so that not everyone can view the detail of candidate to whom a user has voted

    print(response)

    return {
        "data" : response
    }

@app.route('/result', methods=["POST"])

def declareresult():
    data= request.get_json()
    EID = data["EID"]
    CID = data["CID"]
    pwd = data["pwd"]

    res= {}

            
    for i in CID:
        res[i]=0

    for i in userarr:


        if i["type"] == "3" and i["pwd"] == pwd: ##if user is admin he can decrypt and publish result
            
            for i in blockchain:
                temp = i["votes"]
                text = decryption(temp[0]["CID"])
                if temp[0]["EID"] == EID and  text in CID:
                    res.update({text : res[text]+1})
                    print(res[text])
                print(CID)
                print(text)
            return res

    return{
        "msg":"Not authorized to publish result. Admin password missmatched."
        }


if __name__ == "__main__":
    app.run(debug=True)