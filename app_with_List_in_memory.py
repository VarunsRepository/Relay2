from msilib.schema import File
from os import system
from flask import Flask, render_template, request, redirect, url_for, session 
import pandas as pd
from pymongo import MongoClient
import datetime;
 
# ct stores current time
 
app = Flask(__name__)

app.secret_key = 'BAD_SECRET_KEY'

class Message:
    def __init__(self, email, ref, msg, IPAddr):
        self.email = email 
        self.ref   = ref
        self.msg   = msg
        self.IPAddr= IPAddr
        self.timestamp=datetime.datetime.now()
             
Message_List = []

@app.route('/')
def hello_world():
    session["PSW"] ='Hello, Type a message and send hit SEND to relay it OR Hit the RECEIVE Button to fetch it!'
    return redirect("/SendPage")
    #, Title='Hello, Type a message and send hit SEND to relay it OR Hit the RECEIVE Button to fetch it!'
 

@app.route('/SendPage', methods = ['GET', 'POST'])
def SendPage():
    return render_template('Start_Page.html',  title=session["PSW"])


@app.route('/Send', methods = ['POST'])
def Send():
    Email_label = request.form.get("Email_input_Send")
    Reference_label = request.form.get("Reference_input_Send")
    Text_or_Message_input_Send = request.form.get("Text_or_Message_input_Send")
    IPAddr=request.remote_addr
    
    Message_List.append(Message(email=Email_label, ref=Reference_label, msg=Text_or_Message_input_Send, IPAddr=IPAddr))
    print([x.msg for x in  Message_List], "IP address=", IPAddr)

    session["PSW"] = "Message Sent, Don't forget the E-mail or Reference"
    #return redirect("/SendPage")   
    return render_template('Start_Page.html', title = session["PSW"] )

@app.route('/Receive', methods = ['POST'])
def Receive():
    Reference_label = request.form.get("reference_receive")
   
    Current_messages = []
    for x in Message_List:
        if(x.ref == Reference_label):
            Current_messages.append(x.msg)
    
    print(Current_messages)

    session["PSW"] = "Message fetched but still remaining in the queue"
    #return render_template('Start_Page.html',  SearchResults = Current_messages)
    return render_template('Start_Page.html',  SearchResults = Current_messages, title = session["PSW"])

    #return redirect("/SendPage", SearchResults = Current_messages)   
   
if __name__ == "__main__":
   app.run()

   