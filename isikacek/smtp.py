# -*- coding: utf-8 -*-

import configparser
import smtplib
from email.message import EmailMessage

class SimpleSMTP:

    def __init__(self, path):
        self.smtp_config = configparser.ConfigParser()
        self.smtp_config.read(path)

    def send_mail(self, sender, to, subject, body):
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['Sender'] = sender
        msg['From'] = sender
        msg['To'] = to

        c = self.smtp_config['smtp']

        try:
            port = c['port']
        except:
            port = 25

        s = smtplib.SMTP(c['server'], port)

        try:
            tls = c['tls'].strip().lower()
            if tls == 'true' or tls == '1' or tls == 'yes':
                s.starttls()
        except:
            pass
        try:
            user = c['user']
            if user != '':
                s.login(user, c['pass'])
        except:
            pass

        s.send_message(msg)
        s.quit()
