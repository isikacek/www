# -*- coding: utf-8 -*-

from google.appengine.api import mail
from google.appengine.api.app_identity import get_application_id


def send_mail(sender, to, subject, body):
    AN = get_application_id()
    mail.send_mail(
        sender=sender + "@" + AN + ".appspotmail.com",
        to=to,
        subject=subject,
        body=body)
