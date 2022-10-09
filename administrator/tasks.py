from django.core.mail import EmailMessage
from django.template import loader


from celery import shared_task
from celery.utils.log import get_task_logger




logger = get_task_logger(__name__)


@shared_task()
def send_confirmation_mail(subject, new_user,code):
    # sleep()
    mail_subject = subject
    context = {'new_user':new_user,"code":code}
    message = loader.get_template('mail.html').render(context)
    to_email = new_user['email']
    from_email = 'rennintech@gmail.com'
    msg = EmailMessage(mail_subject, message, to=[to_email],from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()
    print("SENIING NOW & SENT")


def send_deal_request_approval_mail(subject, user,deal_request):
    # sleep()
    mail_subject = subject
    context = {'new_user':user,"deal":deal_request}
    message = loader.get_template('mail1.html').render(context)
    to_email = user['email']
    print(to_email)
    from_email = 'rennintech@gmail.com'
    msg = EmailMessage(mail_subject, message, to=[to_email],from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()
    print("SENIING NOW & SENT")