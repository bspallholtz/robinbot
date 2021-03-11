#!/usr/bin/python3.7
import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "brian.stock.algo@gmail.com"
receiver_email = "brian.spallholtz@gmail.com"
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, 'Wear3thechampion$')
    server.sendmail(sender_email, receiver_email, message)
