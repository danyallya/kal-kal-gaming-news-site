import random
import string
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from utils.models import BaseModel


class Profile(AbstractUser):
    birth_date = models.DateField(verbose_name="تاریخ تولد", null=True, blank=True)
    # image = models.ImageField(blank=True, null=True, upload_to='user_images/')
    code = models.CharField(u"کد فراموشی گذرواژه", max_length=200, null=True, blank=True)
    GENDER_CHOICES = (
        ('1', "مذکر"),
        ('2', "مؤنث"),
    )
    gender = models.CharField("جنسیت", default="", choices=GENDER_CHOICES, max_length=50)
    mobile = models.CharField("شماره تماس", max_length=15, null=True, blank=True,
                              validators=[
                                  RegexValidator(
                                      regex='^\d{11}$',
                                      message='شماره تماس اشتباه است',
                                      code='invalid_mobile'
                                  ),
                              ])

    activation_code = models.CharField(u"کد فعال سازی", max_length=200, null=True, blank=True)
    activation_date = models.DateTimeField(verbose_name="تاریخ فعال سازی", null=True, blank=True)
    last_day_message = models.DateField(verbose_name="آخرین تاریخ پیغام دادن", null=True, blank=True)

    activated = models.BooleanField("فعال شده", default=True)

    USER_LEVELS = (
        (1, "تازه ثبت نام کرده"),
        (2, "پیام تایید ایمیل را دیده"),
        (3, "ایمیل را تایید کرده"),
        (4, "اخطار غیرفعال شدن"),
    )

    level = models.IntegerField("سطح", default=3)

    def __str__(self):
        return self.name

    # @property
    # def standard_birth(self):
    #     if self.birth_date:
    #         return self.birth_date.strftime("%Y-%m-%d")

    # @property
    # def age(self):
    #     if self.birth_date:
    #         return date.today().year - self.birth_date.year

    @property
    def name(self):
        return self.first_name or self.username

    def get_android_fields(self):
        return {'u': self.username, 'e': self.email, 'f': self.first_name}
        # @property
        # def profile_image(self):
        #     if self.image:
        #         # print('%s%s' % (settings.MEDIA_URL, self.image))
        #         return '%s%s' % (settings.MEDIA_URL, self.image)
        #     else:
        #         return '/static/img/temp.jpg'

    def create_code(self):
        self.code = ''.join(
            random.choice(string.ascii_letters + string.digits + '(_)][=+') for x in range(50))
        self.save()

    def create_confirm_code(self):
        self.activation_code = ''.join(
            random.choice(string.ascii_letters + string.digits + '(_)][') for x in range(100))
        self.save()


Profile._meta.get_field('first_name').verbose_name = 'نام حقیقی'
Profile._meta.get_field('is_staff').verbose_name = 'وضعیت همکاری'


# class Suggestion(BaseModel):
#     SUGGESTION_TYPES = (
#         (1, "پیشنهاد"),
#         (2, "انتقاد"),
#         (3, "نظر"),
#         (4, "سفارش تبلیغات"),
#     )
#     sug_type = models.IntegerField(verbose_name="نوع", null=True, default=1, choices=SUGGESTION_TYPES)
#     email = models.EmailField(verbose_name=u"ایمیل", null=True)
#     title = models.CharField(verbose_name=u"عنوان", null=True, max_length=700)
#     body = models.TextField(verbose_name=u"متن", null=True, max_length=3000)
#
#     fav = models.BooleanField("علاقه مندی", default=False)
#
#     class Meta:
#         verbose_name = u"تماس با ما"
#         verbose_name_plural = u"تماس با ما"
#
#     def __str__(self):
#         return self.title
#
#
# class Faq(models.Model):
#     question = models.TextField(default="", verbose_name="سوال")
#     answer = models.TextField(default="", verbose_name="پاسخ")
#     order = models.IntegerField(verbose_name="ترتیب", default=1)
#
#     creator = models.ForeignKey('account.Profile', verbose_name="سازنده", null=True, blank=True)
#     created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
#
#     class Meta:
#         verbose_name = "سوالات متداول"
#         verbose_name_plural = "سوالات متداول"
#         ordering = ('order', '-id')
#
#     def __str__(self):
#         return self.question
