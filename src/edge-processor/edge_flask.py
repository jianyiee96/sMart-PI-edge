from flask import Flask, redirect, url_for, request
import firestore_utility
import path_utility
import recommendation_utility
import json, pprint

app = Flask(__name__)
global_items = firestore_utility.get_global_items_dict()
position_item = dict()
for key in global_items.keys():
    value = f"{global_items[key]['posX']},{global_items[key]['posY']}"
    position_item[value] = key

@app.route("/")
def index():
    return "Welcome to sMART's Flask Server"

@app.route('/path')
def path():
    ox = request.args.get('ox')
    oy = request.args.get('oy')
    item = request.args.get('item')
    user = request.args.get('user')
    if item == 'EXIT':
        dx = 99
        dy = 0
    else:
        try:
            dx = global_items[item]['posX']
            dy = global_items[item]['posY']
        except:
            dx = 99
            dy = 0

    print(f"Path request: {ox},{oy} to {dx},{dy}")
    path = path_utility.get_path(int(ox), int(oy), int(dx), int(dy))

    # For recommendation trigger
    user_incart_items = firestore_utility.get_user_incart_items(user)
    item_in_path = set()
    recommend_trigger = set()

    for p in path:
        items_nearby = path_utility.items_nearby(position_item, p['posX'], p['posY'])
        item_in_path = item_in_path.union(items_nearby)

    recommend_trigger = item_in_path - user_incart_items
    print(f"Item in path: {item_in_path}")
    print(f"Item in cart: {user_incart_items}")
    print(f"Item to trigger recommendation: {recommend_trigger}")
    for item in recommend_trigger:
        recommendation_utility.trigger_recommendations(user , item)

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
        dx = 99
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


if __name__ == '__main__':
    app.run(debug = True)
