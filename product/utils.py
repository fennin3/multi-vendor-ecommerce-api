import random,string


def generate_sku():
    sku = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return sku