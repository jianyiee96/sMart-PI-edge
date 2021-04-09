import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import messaging

tokenDatabase = []

cert_path = "../../files/smart-mobile-application-de8a1d29af3c.json"
cred = credentials.Certificate(cert_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_firebase_collection_ref(collection: str):
    """
    Returns the Firebase reference of specified collection.
    """
    return db.collection(collection)

def get_firebase_document_ref(collection: str, document_id: str):
    """
    Returns the Firebase reference of specified collection and document id.
    """
    return db.collection(collection).document(document_id)     


# notifs

from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route("/")
def index():
    return '''
<p>Hello World!</p>
'''

@app.route('/register')
def register():
    userId = request.args.get('userId')
    fcmToken = request.args.get('fcmToken')
    tokenDatabase.append({"userId": userId, "token": fcmToken})
    print("New Token Registered:: User ID: ", userId, ", Token:", fcmToken)
    print(tokenDatabase)
    return userId + ", " + fcmToken

@app.route('/send_notification')
def send_notification():
    userId = request.args.get('userId')
    itemId = request.args.get('itemId')
    print(userId)
    print(itemId)
    recipientToken = ''
    for i in tokenDatabase:
        if i['userId'] == userId:
            recipientToken = i['token']
    print(recipientToken)
    message = messaging.Message(
        data={
            'message': itemId
        },
        token=recipientToken
    )
    print(message)

    response = messaging.send(message)
    print('Successfully sent message:', response)
    return response

if __name__ == '__main__':
   app.run(debug = True)
