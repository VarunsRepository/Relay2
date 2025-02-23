#from os import system
from flask import Flask, render_template, request, redirect, session, jsonify #, url_for
#from pymongo.mongo_client import MongoClient
#from pymongo.server_api import ServerApi
from pymongo import MongoClient
import datetime;

from flask_restful import Resource, Api, reqparse




# URI for the Relay2App DataBase
#uri = "mongodb+srv://<<###Redacted ConnectionString to MongoDB Database tha is used by the App/API###>>"
#uri = "mongodb+srv://<<###Redacted ConnectionString to MongoDB Database tha is used by the App/API###>>"
# Create a new client and connect to the server
#client2 = MongoClient(uri) #, server_api=ServerApi('1'))
#DB = client2["Relay2AppDB"]
#Messages = DB.MesagesCollection

# ct stores current time
app = Flask(__name__)
api= Api(app)
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
    try:
        print("Invoked Send Method")
        Email_label = request.form.get("Email_input_Send")
        Reference_label = request.form.get("Reference_input_Send")
        Text_or_Message_input_Send = request.form.get("Text_or_Message_input_Send")
        IPAddr=request.remote_addr

        Message_List.append(Message(email=Email_label, ref=Reference_label, msg=Text_or_Message_input_Send, IPAddr=IPAddr))
        print([x.msg for x in  Message_List], "IP address=", IPAddr)

        uri = "mongodb+srv://<<###Redacted ConnectionString to MongoDB Database tha is used by the App/API###>>"
        client2 = MongoClient(uri) #, server_api=ServerApi('1'))
        DB = client2["Relay2AppDB"]
        Messages = DB.MesagesCollection

        Messages.insert_one(
            {
            "email"     :Email_label,
            "ref"       :Reference_label,
            "msg"       :Text_or_Message_input_Send,
            "IPAddr"    :IPAddr,
            "timestamp" :datetime.datetime.now()
            }
            )


        session["PSW"] = "Message Sent, Don't forget the E-mail or Reference"
        #return redirect("/SendPage")
        return render_template('Start_Page.html', title = session["PSW"] )
    except Exception as inst:
        print(type(inst))    # the exception type
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
        # but may be overridden in exception subclasses
        x, y = inst.args     # unpack args
        print("Something else went wrong")

@app.route('/Receive', methods = ['POST'])
def Receive():
    try:
        print("Invoked Receive Method")
        Reference_label = request.form.get("reference_receive")

        Current_messages = []
        for x in Message_List:
            if(x.ref == Reference_label):
                Current_messages.append(x.msg)

        uri = "mongodb+srv://<<###Redacted ConnectionString to MongoDB Database tha is used by the App/API###>>"
        client2 = MongoClient(uri) #, server_api=ServerApi('1'))
        DB = client2["Relay2AppDB"]
        Messages = DB.MesagesCollection

        fetched_messages_documents = Messages.find({"ref" :Reference_label})

        fetched_messages = [x['msg'] for x in fetched_messages_documents ]

        print(fetched_messages)

        session["PSW"] = "Message fetched but still remaining in the queue"
        #return render_template('Start_Page.html',  SearchResults = Current_messages)
        return render_template('Start_Page.html',  SearchResults = fetched_messages, title = session["PSW"])

        #return redirect("/SendPage", SearchResults = Current_messages)
    except Exception as inst:
        print(type(inst))    # the exception type
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
                             # but may be overridden in exception subclasses
        #x, y = inst.args     # unpack args
        print("Something else went wrong")


###API CODE STARTS HERE :

class Read_Message(Resource):

    def post(self):
        try:
            print("Invoked Read Message API")

            email = ""
            ref   = ""
            msg   = ""

            Incomming_Request = request.get_json()

            if("email" in Incomming_Request.keys()):
                email = Incomming_Request["email"]

            if("ref" in Incomming_Request.keys()):
                ref = Incomming_Request["ref"]

            print("1. ", request.headers)

            uri = "mongodb+srv://<<Redacted Database ConnectionString for MongoDB Database >>"
            client2 = MongoClient(uri) #, server_api=ServerApi('1'))
            DB = client2["Relay2AppDB"]
            Messages_Collection = DB.MesagesCollection
            fetched_messages_documents = Messages_Collection.find({"ref" :ref})
            print("Message search completed")

            fetched_messages = [x['msg'] for x in fetched_messages_documents ]

            return (jsonify( str( fetched_messages) ) )


        except Exception as inst:
            print("2. ", request.headers)
            print(type(inst))    # the exception type
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
            # but may be overridden in exception subclasses
            x, y = inst.args     # unpack args
            print("Something else went wrong")


class Send_Message(Resource):

    def post(self):
        try:
            print("Invoked Send Message API")
            #Email_label = request.form.get("Email_input_Send")
            #Reference_label = request.form.get("Reference_input_Send")
            #Text_or_Message_input_Send = request.form.get("Text_or_Message_input_Send")
            #IPAddr=request.remote_addr


            #Message_List.append(Message(email=Email_label, ref=Reference_label, msg=Text_or_Message_input_Send, IPAddr=IPAddr))
            #print([x.msg for x in  Message_List], "IP address=", IPAddr)

            email = ""
            ref   = ""
            msg   = ""

            Incomming_data = request.get_json()

            if("email" in Incomming_data.keys()):
                email = Incomming_data["email"]

            if("ref" in Incomming_data.keys()):
                ref = Incomming_data["ref"]

            if("msg" in Incomming_data.keys()):
                msg = Incomming_data["msg"]


            Date_to_store_In_Mongo_Collection = {
            "email"              : str( email) ,
            "ref"                : str( ref  ) ,
            "msg"                : str( msg  ) ,
            "IPAddr"             : str( request.remote_addr ),
            "timestamp"          : str( datetime.datetime.now() ),
            "request_headers"    : str( request.headers                     )
            #"Cookies"            : str( request.Cookies                     ),
            #"Environ"            : str( request.Environ                     ),
            #"Method"             : str( request.Method                     )
            }


            uri = "mongodb+srv://<<###Redacted ConnectionString to MongoDB Database tha is used by the App/API###>>"
            client2 = MongoClient(uri) #, server_api=ServerApi('1'))
            DB = client2["Relay2AppDB"]
            Messages_Collection = DB.MesagesCollection
            Messages_Collection.insert_one(Date_to_store_In_Mongo_Collection)
            print("Object successfully stored in MongoDB Collection")

            return (jsonify( str( Date_to_store_In_Mongo_Collection) ) )

            #return (data["Text_or_Message_input_Send"])

            #session["PSW"] = "Message Sent, Don't forget the E-mail or Reference"
            ##return redirect("/SendPage")
            #return render_template('Start_Page.html', title = session["PSW"] )
        except Exception as inst:
            print(type(inst))    # the exception type
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
            # but may be overridden in exception subclasses
            x, y = inst.args     # unpack args
            print("Something else went wrong")


@app.route('/Console', methods = ['GET', 'POST'])
def Console():
    return render_template('console.html')


api.add_resource(Read_Message, '/ReadMessageAPI')
api.add_resource(Send_Message, '/SendMessageAPI' )


if __name__ == "__main__":
   app.run()

