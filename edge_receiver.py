import firestore_utility  

def update_cart_items(cart_name: str, cart_items: dict):

    user_id = get_cart_current_user(cart_name)

    if(user_id is None):
        return None

    cart_items_ref = firestore_utility.get_firebase_document_ref("users", user_id).collection("cartItems")

    items = cart_items_ref.stream()
    for item in items:
        curr_item_dict = item.to_dict()

        if item.id in cart_items:
            curr_item_dict['quantityInCart'] = cart_items[item.id]
            cart_items_ref.document(item.id).set(curr_item_dict)
        elif curr_item_dict['quantity'] == 0:
            cart_items_ref.document(item.id).delete()
        elif curr_item_dict['quantity'] != 0:
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
    except:
        return None

def get_global_items_dict():
    items_collection_ref = firestore_utility.get_firebase_collection_ref("items")
    items = items_collection_ref.stream()
    item_dict = dict()
    for item in items:
        item_dict[item.id] = item.to_dict()
    return item_dict

global_items = get_global_items_dict()

# l = ['MP1WsknTkMqlvom70wDq',
#     'OyVCNQgJ80lWy9HjbpvF',
#     'PXmYk7IzzsrHFMq5j70o',
#     'VfgrHcX6LvHuAvkJtdgU',
#     'YvxptylcQC7o6s7fK7H9',
#     'oZGiQLJMymfo2Mc4KJYm'
#     ]

cart_name = "CART_001"
d = dict()
# d['OyVCNQgJ80lWy9HjbpvF'] = 3
# d['MP1WsknTkMqlvom70wDq'] = 3
# d['VfgrHcX6LvHuAvkJtdgU'] = 3

update_cart_items(cart_name, d)
