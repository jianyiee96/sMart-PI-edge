from flask import Flask, redirect, url_for, request
import firestore_utility as firestore_utility
import path_utility as path_utility


app = Flask(__name__)
token_database = []

@app.route("/")
def index():
    return "Welcome to sMART's Flask Server"

@app.route('/register')
def register():
    user_id = request.args.get('userId')
    fcm_token = request.args.get('fcmToken')
    token_database.append({"userId": user_id, "token": fcm_token})
    print(f"New Token Registered: User ID: {user_id}, Token: {fcm_token}")
    return user_id + ", " + fcm_token

@app.route('/send_notification')
def send_notification():
    user_id = request.args.get('userId')
    item_id = request.args.get('itemId')
    recipient_token = ''
    for i in token_database:
        if i['userId'] == user_id:
            recipient_token = i['token']
    message = firestore_utility.messaging.Message(
        data={
            'message': item_id
        },
        token=recipient_token
    )
    print(message)
    response = firestore_utility.messenging.send(message)
    print(f'Successfully sent message: {response}')
    return response

@app.route('/path')
def path():
    ox = request.args.get('ox')
    oy = request.args.get('oy')
    dx = request.args.get('dx')
    dy = request.args.get('dy')
    print(f"Path request: {ox},{oy} to {dx},{dy}")
    path = path_utility.get_path(int(ox), int(oy), int(dx), int(dy))
    return str(path)

@app.route('/path2')
def path_ui():
    ox = request.args.get('ox')
    oy = request.args.get('oy')
    dx = request.args.get('dx')
    dy = request.args.get('dy')
    print(f"Path2 request: {ox},{oy} to {dx},{dy}")
    path = path_utility.get_path(int(ox), int(oy), int(dx), int(dy))
    if(len(path) == 1):
        return str(path)

    path_ui = path_utility.apply_path(path)[1:-1].replace("],","<br>").replace("[","").replace(",","").replace("]","")

    html = '<html><head><!-- Hi Are you bored? --></head><body>'
    html += '<div style="outline-style: solid; font-family: monospace; display: oinline-block">'
    html += path_ui
    html += '</div>'
    html += '</body></html>'

    return html


@app.route('/raw')
def path_ui_raw():

    path_ui = path_utility.getmap()[1:-1].replace("],","<br>").replace("[","").replace(",","").replace("]","")

    html = '<html><head><!-- Hi Are you bored? --></head><body>'
    html += '<div style="outline-style: solid; font-family: monospace; display: oinline-block">'
    html += path_ui
    html += '</div>'
    html += '</body></html>'

    return html

if __name__ == '__main__':
    app.run(debug = True)