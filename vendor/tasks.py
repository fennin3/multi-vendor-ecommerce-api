from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template import Context, loader
from django.template.loader import render_to_string, get_template


from celery import current_app, shared_task
from celery.utils.log import get_task_logger
from time import sleep




logger = get_task_logger(__name__)


@shared_task()
def send_confirmation_mail(subject, new_user,code):
    mail_subject = subject
    context = {'new_user':new_user,"code":code}
    message = loader.get_template('mail.html').render(context)
    to_email = new_user['email']
    from_email = 'rennintech@gmail.com'
    msg = EmailMessage(mail_subject, message, to=[to_email],from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()
    print("SENIING NOW & SENT")