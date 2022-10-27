import random,string


def generate_order_id():
    sku = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    return sku