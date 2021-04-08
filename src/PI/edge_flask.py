from flask import Flask, redirect, url_for, request
import firestore_utility as firestore_utility
import path_utility as path_utility
import json, pprint

app = Flask(__name__)
token_database = []
global_items = firestore_utility.get_global_items_dict()
position_item = dict()
for key in global_items.keys():
    value = f"{global_items[key]['posX']},{global_items[key]['posY']}"
    position_item[value] = key

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
    item = request.args.get('item')
    user = request.args.get('user')
    try:
        dx = global_items[item]['posX']
        dy = global_items[item]['posY']
    except:
        dx = 0
        dy = 0

    print(f"Path request: {ox},{oy} to {dx},{dy}")
    path = path_utility.get_path(int(ox), int(oy), int(dx), int(dy))

    # For recommendation trigger
    user_incart_items = set()
    item_in_path = set()
    recommend_trigger = set()

    cart_items_ref = firestore_utility.get_firebase_document_ref("users", user).collection("cartItems")
    items = cart_items_ref.stream()
    for i in items:
        user_incart_items.add(i.id)

    for p in path:
        if f"{p['posX']},{p['posY']}" in position_item:
            item_in_path.add(position_item[f"{p['posX']},{p['posY']}"])

    recommend_trigger = item_in_path - user_incart_items
    print(f"Item in path: {item_in_path}")
    print(f"Item in cart: {user_incart_items}")
    print(f"Item to trigger recommendation: {recommend_trigger}") # TO-DO add api call here
    return json.dumps({'item':item,'path':path})

@app.route('/path2')
def path_ui():
    ox = request.args.get('ox')
    oy = request.args.get('oy')
    item = request.args.get('item')
    try:
        dx = global_items[item]['posX']
        dy = global_items[item]['posY']
    except:
        dx = 0
        dy = 0

    print(f"UI Path request: {ox},{oy} to {dx},{dy}")
    path = path_utility.get_path(int(ox), int(oy), int(dx), int(dy))
    path_ui = path_utility.apply_path(path)[1:-1].replace("],","<br>").replace("[","").replace(",","").replace("]","")
    html = '<html><head></head><body>'
    html += '<div style="outline-style: solid; font-family: monospace; display: oinline-block">'
    html += path_ui
    html += '</div>'
    html += '</body></html>'
    return html

@app.route('/initNavigate')
def init_navigate():
    try:
        ox = request.args.get('ox')
        oy = request.args.get('oy')
        user_id = request.args.get('user')
        cart_items_ref = firestore_utility.get_firebase_document_ref("users", user_id).collection("cartItems")
        items = cart_items_ref.stream()
        item_distance_dict = dict()
        for i in items:
            dx = global_items[i.id]['posX']
            dy = global_items[i.id]['posY']
            path = path_utility.get_path(int(ox), int(oy), int(dx), int(dy))
            item_distance_dict[i.id] = len(path)
        pprint.pprint(item_distance_dict)
        dist_sorted = sorted(item_distance_dict.items(), key=lambda i: i[1])
        sorted_index = dict()
        idx = 0
        for i in dist_sorted:
            sorted_index[i[0]] = idx
            idx += 1
        items = cart_items_ref.stream()
        for i in items:
            curr_item_dict = i.to_dict()
            curr_item_dict['sortIdx'] = sorted_index[i.id]
            cart_items_ref.document(i.id).set(curr_item_dict)
        return json.dumps({'status':1})
    except:
        return json.dumps({'status':-1})

@app.route('/is4151grade')
def grade():
    from random import randrange
    x = randrange(10)
    if x == 0:
        return "A+"
    elif x == 1: 
        return "A"
    elif x == 2:
        return "A-"
    elif x == 3:
        return "B+"
    elif x == 4:
        return "B"
    elif x == 5:
        return "B-"
    elif x == 6:
        return "C"
    elif x == 7:
        return "D"
    elif x == 8:
        return "E"
    elif x == 9:
        return "F"
    else:
        return "F-"

if __name__ == '__main__':
    app.run(debug = True)
