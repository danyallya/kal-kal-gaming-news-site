# -*- coding:utf-8 -*-
import threading
from urllib import request
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from account.models import Profile

__author__ = 'M.Y'


class MessageServices(threading.Thread):
    from_email = 'noreply@manzoom.ir'
    admin_email = 'noreply@manzoom.ir'

    def __init__(self, email):
        threading.Thread.__init__(self)
        self.email = email

    # def start(self):
    #     self.run()

    def run(self):
        try:
            user = Profile.objects.get(email=self.email)
            user.create_code()

            url = settings.SITE_URL + "/change_pass/?c=" + request.quote(user.code)
            message = u"""
                <!DOCTYPE html>
                <html dir="ltr" lang="fa-ir">
                <head><meta charset="utf-8"></head>
                <body>
                <div style="direction:rtl;font-family:tahoma;font-size:17px;">
                باسلام
                <br/>
شما درخواست فراموشی رمز عبور را ارسال کرده اید.
    <br/>
    با استفاده از لینک زیر می توانید رمز عبور خود را تغییر دهید.
                    <br/><br/>
                    <br/>
                    <a href="%s">لینک به صفحه تغییر رمز عبور</a>

                    <br/>
                    <br/>
                    <br/>
                    موفق باشید
                </div>
                </body>
                </html>
                """ % url
            msg = EmailMultiAlternatives(subject=u"تغییر رمز عبور در منظوم", body='',
                                         from_email=MessageServices.from_email,
                                         to=[user.email])
            msg.attach_alternative(message, "text/html")
            msg.send()
        except Exception as s:
            print(s)


class SendConfirmationServices(threading.Thread):
    from_email = 'noreply@manzoom.ir'
    admin_email = 'noreply@manzoom.ir'

    def __init__(self, email):
        threading.Thread.__init__(self)
        self.email = email

    def run(self):
        try:
            user = Profile.objects.get(email=self.email)

            url = settings.SITE_URL + reverse("confirm_account") + "?c=" + request.quote(user.activation_code)

            message = u"""
                <!DOCTYPE html>
                <html dir="ltr" lang="fa-ir">
                <head><meta charset="utf-8"></head>
                <body>
                <div style="direction:rtl;font-family:tahoma;font-size:17px;">
                باسلام
                <br/>
                برای فعال سازی حساب کاربری خود در منظوم روی لینک زیر کلیک کنید
                    <br/>
                    <br/><br/>
                    <br/>
                    <a href="%s">لینک فعال سازی حساب کاربری</a>

                    <br/>
                    <br/>
                    <br/>
                    باتشکر
                </div>
                </body>
                </html>
                """ % url
            msg = EmailMultiAlternatives(subject=u"فعال سازی حساب کاربری در منظوم", body='',
                                         from_email=MessageServices.from_email,
                                         to=[user.email])
            msg.attach_alternative(message, "text/html")
            msg.send()
        except Exception as s:
            print(s)

# from django.core.mail.message import EmailMultiAlternatives
#
# msg = EmailMultiAlternatives(subject=u"asdgdsgsg", body='',
#                              from_email='noreply@manzoom.ir',
#                              to=['mymy47@gmail.com'])
# msg.attach_alternative("sadgsg", "text/html")
# msg.send()
