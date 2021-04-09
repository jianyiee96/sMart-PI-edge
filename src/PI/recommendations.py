import firestore_utility
import pandas as pd
import requests
import numpy as np

items = firestore_utility.get_global_items_dict()
df = pd.DataFrame.from_dict(items, orient='index')
tx_history = [];

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
        load_notification_payload(1, most_expensive_item_id)
        return most_expensive_item_id
    else:
        return item_id

# if the item is not the cheapest, then recommend the cheapest
def recommend_cheapest(item_id, category):
    cheapest_item_id = item_id_with_min_price(category)
    if item_id != cheapest_item_id:
        load_notification_payload(1, cheapest_item_id)
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

# if the item is not on promotion, recommend all the items that are on promotion
def recommend_promotion(item_id, category):
    if item_on_promotion(item_id) == False:
        temp_items = df[df['category'] == category]
        print(temp_items)
        for item in temp_items.index:
            if item != item_id:
                if item_on_promotion(item):
                    load_notification_payload(1, item)
                    print(item)

def recommend_bigger_purchase_from_past_purchases():
    return

def recommend_monthly_purchase():
    return

# load and send the notification payload
def load_notification_payload(user_id, item_id):
    payload = {'userId': user_id, 'itemId': item_id}
    r = requests.get('http://localhost:5000/send_notification', params=payload)
    print(r.url)
