import pandas

def load_device_cart_mapping():
    device_cart_mapping = dict()
    device_cart_df = pandas.read_excel('files/mapping.xlsx', sheet_name='device_cart')
    devices = device_cart_df['device'].tolist()
    carts = device_cart_df['cart'].tolist()
    for device, cart in zip(devices, carts):
        device_cart_mapping[device] = cart
    return device_cart_mapping

def load_rfid_item_mapping():
    rfid_item_mapping = dict()
    rfid_item_df = pandas.read_excel('files/mapping.xlsx', sheet_name='rfid_item')
    rfids = rfid_item_df['rfid'].tolist()
    items = rfid_item_df['item'].tolist()
    for rfid, items in zip(rfids, items):
        rfid_item_mapping[rfid] = items
    return rfid_item_mapping