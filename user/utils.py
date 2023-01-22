from django.core.mail import send_mail


def send_verification(data):
    send_mail(
    subject=data['subject'],
    message=data['body'],
    from_email=data['from_email'],
    recipient_list=[data['to_email'],],
    # html_message=(data['html_msg'],html_msg.html)
    )