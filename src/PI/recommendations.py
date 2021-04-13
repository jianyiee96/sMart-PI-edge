import firestore_utility
import pandas as pd
import numpy as np
import requests

items = firestore_utility.get_global_items_dict()
df = pd.DataFrame.from_dict(items, orient='index')
tx_history = [];

# Put a 5 minutes check so user dont get more than 1 recommendation in 5 minutes window.
# Recommendation history is used to prevent user from getting repeated recommendation for REC_TYPE an REC_ITEM
# For each Recommendation, check through this reocmmendation history
recommendation_history = {
    'user_id' : [
        {"rec_type" : "path",
        "rec_item" : "item_id 1",
        "timestamp" : "12:00pm"
        },
        {"rec_type" : "adding_item",
        "rec_item" : "item_id 2",
        "timestamp" : "12:30pm"
        },
    ],
    'user_id 2' : [
        {"rec_type" : "path",
        "rec_item" : "item_id 1",
        "timestamp" : "12:00pm"
        },
        {"rec_type" : "adding_item",
        "rec_item" : "item_id 2",
        "timestamp" : "12:30pm"
        },
    ],
}

def reset_user_recommendation(user: str):
    recommendation_history[user] = list()

def send_notification(user: str, header: str, message: str, item: str):
    message = firestore_utility.messaging.Message(
        data={
            'header' : header,
            'message': message,
            'itemId': item
        },
        token=firestore_utility.get_user_fms_token(user)
    )
    firestore_utility.messaging.send(message)

# returns the item_id of the item with the max price in the category
def item_id_with_max_price(category):
    temp_items = df[df['category'] == category]
    max_value = temp_items['price'].max()
    return df[df['price'] == max_value].iloc[0].name

# returns the item_id of the item with the min price in the category
def item_id_with_min_price(category):
    temp_items = df[df['category'] == category]
    min_value = temp_items['price'].min()
    return df[df['price'] == min_value].iloc[0].name

# if the item is not the most expensive, then recommend the most expensive
def recommend_most_expensive(item_id, category):
    most_expensive_item_id = item_id_with_max_price(category)
    if item_id != most_expensive_item_id:
        # load_notification_payload(1, most_expensive_item_id)
        return most_expensive_item_id
    else:
        return item_id

# if the item is not the cheapest, then recommend the cheapest
def recommend_cheapest(item_id, category):
    cheapest_item_id = item_id_with_min_price(category)
    if item_id != cheapest_item_id:
        # to complete
        # send_notification()
        return cheapest_item_id
    else:
        return item_id

# checks if item is on promotion or not
def item_on_promotion(item_id):
    temp_items = df.loc[item_id]
    if temp_items.oldPrice != 0:
        return True
    else:
        return False

# if the item is not on promotion, recommend the cheapest item on promotion
def recommend_promotion(item_id, category):
    min_item = item_id
    temp_items = df[df['category'] == category]
    min_item_price = temp_items['price'].max()
    for item in temp_items.index:
        if item != item_id:
            if item_on_promotion(item):
                item_price = df.loc[item_id].price
                if item_price <= min_item_price:
                    min_item_price = item_price
                    min_item = item
    return min_item

def recommend_milk_from_cereal():
    return 'OyVCNQgJ80lWy9HjbpvF'

def recommend_bigger_purchase_from_past_purchases():
    return

def recommend_monthly_purchase():
    return

def trigger_recommendations(user_id: str, item_id: str):
    profile_pref = firestore_utility.get_firebase_document_ref("users", user_id).get(field_paths={"profile_habit"}).to_dict()['profile_habit']
    item_cat = firestore_utility.get_firebase_document_ref("items", item_id).get(field_paths={"category"}).to_dict()['category']
    print("User Id: ", user_id)
    print("User profile pref: ", profile_pref)
    print("Item Id: ", item_id)
    print("Item Category: ", item_cat)

    items_in_cart = firestore_utility.get_user_incart_items(user_id)
    print(items_in_cart)

    # only the most expensive items
    if profile_pref == 'QUALITY':
        item_to_reco = recommend_most_expensive(item_id, item_cat)
        item_to_reco_name = firestore_utility.get_firebase_document_ref("items", item_to_reco).get(field_paths={"name"}).to_dict()[
            'name']
        if item_to_reco not in items_in_cart:
            send_notification(user_id,
                                              "Just for you",
                                              "How about something a little better?"
                                              + "\n" + item_to_reco_name,
                                              item_to_reco
                                              )
    # only the cheapest items
    elif profile_pref == 'SAVER':
        item_to_reco = recommend_cheapest(item_id, item_cat)
        item_to_reco_name = firestore_utility.get_firebase_document_ref("items", item_to_reco).get(field_paths={"name"}).to_dict()[
            'name']
        if item_to_reco not in items_in_cart:
            send_notification(user_id,
                                              "Just for you",
                                              "How about something a little cheaper?"
                                              + "\n" + item_to_reco_name,
                                              item_to_reco
                                              )
    # only promotion items and the cheapest promo item
    elif profile_pref == 'MODERATE':
        item_to_reco = recommend_promotion(item_id, item_cat)
        item_to_reco_name = firestore_utility.get_firebase_document_ref("items", item_to_reco).get(field_paths={"name"}).to_dict()[
            'name']
        print(item_to_reco)
        if item_to_reco not in items_in_cart:
            send_notification(user_id,
                                              "Just for you",
                                              "How about this promotion item?"
                                              + "\n" + item_to_reco_name,
                                              item_to_reco
                                              )

    # CEREAL RECCO

    # if the item put in is CEREAL
    if item_id == 'RMWLUuACH72OuqSPYQDk' or item_id == 'rxRod7cigQjBK9dDmlHv':
        # check for presence of milk
        print("CEREAL ITEM ID CHECK:" , item_id)
        if 'OyVCNQgJ80lWy9HjbpvF' in items_in_cart or 'VfgrHcX6LvHuAvkJtdgU' in items_in_cart:
            pass
        else:
            item_to_reco = recommend_milk_from_cereal()
            item_to_reco_name = firestore_utility.get_firebase_document_ref("items", item_to_reco).get(field_paths={"name"}).to_dict()[
            'name']
            send_notification(user_id,
                                              "I sense cereal!",
                                              "Would you like this to go with..."
                                              + "\n" + item_to_reco_name,
                                              item_to_reco
                                              )
