import pandas

def load_device_cart_mapping():
    device_cart_mapping = dict()
    device_cart_df = pandas.read_excel('files/mapping.xlsx', sheet_name='device_cart')
    for _, row in device_cart_df.iterrows():
        device_cart_mapping[row['device']] = row['cart']
    return device_cart_mapping

def load_rfid_item_mapping():
    rfid_item_mapping = dict()
    rfid_item_df = pandas.read_excel('files/mapping.xlsx', sheet_name='rfid_item')
    for _, row in rfid_item_df.iterrows():
        rfid_item_mapping[row['rfid']] = row['item']
    return rfid_item_mapping