from django.core.mail import send_mail
from django.template.loader import render_to_string
import uuid



import random


def send_confirmation_code(user):
    print(f'From: hello@multivendor.io\nto: {user.email}\nConfirmation Code: {user.confirmation_code}')


def generate_uuid():
    code = 'VN' + str(uuid.uuid4()).split('-')[-1]
    return code

#Generate account confirmation code
def gen_confirmation_code():
    cc =  random.randrange(100000, 999999)
    return cc