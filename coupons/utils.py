import random,string



def generate_coupon_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return code
