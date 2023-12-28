import smtplib
from celery import Celery
from email.message import EmailMessage

from config import SMTP_EMAIL,SMTP_PASSWORD

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')


def text_email(user):
    email = EmailMessage()
    email['Subject'] = "Ayons asperges pour le déjeuner"
    email['From'] = SMTP_EMAIL
    email['To'] = SMTP_EMAIL
    email.set_content('Salut!'+f'{user}')
    return email


@celery.task
def sent_email(user: str):
    email = text_email(user)
    with smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT) as s:
        s.login(SMTP_EMAIL, SMTP_PASSWORD)
        s.send_message(email)