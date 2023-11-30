# -*- coding:utf-8 -*-
# @Time : 2023/11/29 16:58
# @File : EmailNotification.py

# The inspiration comes from: https://www.youtube.com/watch?v=g_j6ILT-X0k
# Check the link above for setting up an "app password" for your account.

from email.message import EmailMessage
import os
import ssl
import smtplib

SENDER = 'felix.shuhui.lin@gmail.com'
PASSWORD = os.environ.get("GMAIL_PASSWORD_SHUHUI")

receiver_email = 'shuhuilin@uchicago.edu'


def notify(receiver_email):
    subject = "wasssssssup!"
    body = "It's a prank lol"

    em = EmailMessage()
    em['From'] = SENDER
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    # Connect to the SMTP server (Gmail example)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.sendmail(SENDER, receiver_email, em.as_string())


# notify(receiver_email)
