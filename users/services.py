from email.message import EmailMessage
from django.conf import settings
import ssl
import smtplib


def send_an_email(subject, body, send_to):
    sender = settings.MY_EMAIL
    password = settings.EMAIL_PASSWORD
    em = EmailMessage()
    em['To'] = send_to
    em['From'] = sender
    em['Subject'] = subject
    em.set_content(body)
    
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, send_to, em.as_string())
