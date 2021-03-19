import firestore_utility as firestore_utility
import excel_utility as excel_utility
import serial, pprint

def update_cart_items(cart_name: str, cart_items: dict):
    """
    cart_name: "CART_001" / "CART_002"
    cart_items: {
        'OyVCNQgJ80lWy9HjbpvF' : 4.
        'VfgrHcX6LvHuAvkJtdgU' : 2
    }

    Does not update item quantity if the quantity does not change.
    When updating, iterates the existing list of items that is in Firestore, process item if its in supplied dict
    For unprocessed items, will add each of them and their quantity in cart into Firestore
    """
    user_id = get_cart_current_user(cart_name)
    cart_items = cart_items.copy()

    if(user_id is None):
        return None

    cart_items_ref = firestore_utility.get_firebase_document_ref("users", user_id).collection("cartItems")

    items = cart_items_ref.stream()
    
    for item in items:
        curr_item_dict = item.to_dict()

        if item.id in cart_items:
            if curr_item_dict['quantityInCart'] != cart_items[item.id]:
                curr_item_dict['quantityInCart'] = cart_items[item.id]
                cart_items_ref.document(item.id).set(curr_item_dict)
        elif curr_item_dict['quantity'] == 0:
            cart_items_ref.document(item.id).delete()
        elif curr_item_dict['quantity'] != 0:
            if curr_item_dict['quantityInCart'] != 0:
                curr_item_dict['quantityInCart'] = 0
                cart_items_ref.document(item.id).set(curr_item_dict)
        
        cart_items.pop(item.id, None)

    for extra_item_id in cart_items:
        extra_item = global_items[extra_item_id].copy()
        extra_item['quantity'] = 0
        extra_item['quantityInCart'] = cart_items[extra_item_id]
        cart_items_ref.document(extra_item_id).set(extra_item)

def get_cart_current_user(cart_name: str):
    try:
        cart_document_ref = firestore_utility.get_firebase_document_ref("carts", cart_name)
        return cart_document_ref.get().to_dict()['user']
    except Exception:
        return None

def get_global_items_dict():
    items_collection_ref = firestore_utility.get_firebase_collection_ref("items")
    items = items_collection_ref.stream()
    item_dict = dict()
    for item in items:
        item_dict[item.id] = item.to_dict()
    return item_dict

if __name__ == '__main__':
    global_items = get_global_items_dict()
    cart_session = dict()
    device_cart_mapping = excel_utility.load_device_cart_mapping()
    rfid_item_mapping = excel_utility.load_rfid_item_mapping()

    ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
    print("PI-EDGE is running.. Listening on serial port.")
    while True:
        
        response = ser.readline()
        response = response.decode('utf-8').strip()
        if(response != '' and response[0] == '>'):
            response_comp = response[1:].split("=")

            cart_name = device_cart_mapping[response_comp[0]]
            command = response_comp[1]
            item = rfid_item_mapping[response_comp[2]]
            print()
            print(f"Command: {command}")
            print(f"Cart: {cart_name} ({response_comp[0]})")
            print(f"Item: {item} ({response_comp[2]})" )

            if cart_name not in cart_session:
                cart_session[cart_name] = dict()
                print("New session for " +  cart_name)

            if(command == 'A'):
                if item in cart_session[cart_name]:
                    cart_session[cart_name][item] += 1
                else:
                    cart_session[cart_name][item] = 1
            elif(command == 'R'):
                cart_session[cart_name][item] -= 1
                if(cart_session[cart_name][item] == 0):
                    cart_session[cart_name].pop(item, None)
            print(f"{cart_name} all items:")
            pprint.pprint(cart_session[cart_name])
            update_cart_items(cart_name, cart_session[cart_name])

