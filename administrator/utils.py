from enum import Enum
# from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.utils.encoding import force_bytes, force_text
from django.template import loader
# from django.template.loader import render_to_string, get_template




class STATUS(Enum):
    PENDING = 'pending'
    ORDER_PLACED = 'order_placed'
    ORDER_CONFIRMED = 'order_confirmed'
    PROCESSED = 'processed'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    ORDER_RETURNED = 'order_returned'
    REFUNDED = 'refunded'


def send_mail(subject, user, template):

    mail_subject = subject
    context = {'new_user':user}
    message = loader.get_template(template).render(context)
    to_email = user.email
    from_email = 'hello@multivendor.io'
    msg = EmailMessage(mail_subject, message, to=[to_email],from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()