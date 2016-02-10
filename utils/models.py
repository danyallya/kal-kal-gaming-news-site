import json
import random
import string

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.transaction import atomic
from solo.models import SingletonModel


class Named(models.Model):
    name = models.CharField(verbose_name="نام", max_length=500)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class LogModel(models.Model):
    creator = models.ForeignKey('account.Profile', verbose_name="سازنده", null=True, blank=True)
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)

    class Meta:
        abstract = True


class BaseModel(Named, LogModel):
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def update(self):
        pass

    @classmethod
    @atomic
    def update_all(cls):
        for obj in cls.objects.all():
            obj.update()

    @staticmethod
    def get_summery_json(objs, user):
        data = []
        for obj in objs:
            data.append(obj.get_summery_fields(user))
        return json.dumps(data)

    @classmethod
    @atomic
    def update_all_codes(cls):
        for obj in cls.objects.all():
            obj.update_code()

    def update_code(self):
        if hasattr(self, 'code') and not self.code:
            self.code = generate_code()
            self.save()


def generate_code():
    return ''.join(random.sample(string.digits, 7))


# class SiteConfig(SingletonModel):
#     pass
#
#     class Meta:
#         verbose_name = "تنظیمات سایت"
#
#     def __str__(self):
#         return "تنظیمات سایت"
#
#     @classmethod
#     def update(cls):
#         config = SiteConfig.get_solo()
#
#         config.save()


# class VisitorTrack(models.Model):
#     site_visitor_count = models.IntegerField("تعداد بازدید سایت", default=0)
#     app_visitor_count = models.IntegerField("تعداد بازدید از نرم افزار", default=0)
#
#     visitor_count = models.IntegerField("تعداد بازدید", default=0)
#
#     class Meta:
#         abstract = True
#
#     def add_app_visit(self, request, content_type):
#         UpdateAppVisit(self, request, content_type).start()
#
#     def add_site_visit(self, request, content_type):
#         UpdateSiteVisit(self, request, content_type).start()
#
#
# class UpdateSiteVisit(threading.Thread):
#     def __init__(self, obj, request, content_type):
#         threading.Thread.__init__(self)
#         self.content_type = content_type
#         self.request = request
#         self.obj = obj
#
#     def run(self):
#         user = None
#         if self.request.user.is_authenticated():
#             user = self.request.user
#
#         VisitLog.objects.create(content_type=self.content_type, ip_address=get_client_ip(self.request),
#                                 object_pk=self.obj.id, user=user)
#
#         self.obj.site_visitor_count += 1
#
#         self.obj.visitor_count = self.obj.app_visitor_count + self.obj.site_visitor_count
#
#         self.obj.save()
#
#
# class UpdateAppVisit(threading.Thread):
#     def __init__(self, obj, request, content_type):
#         threading.Thread.__init__(self)
#         self.content_type = content_type
#         self.request = request
#         self.obj = obj
#
#     def run(self):
#         user = None
#         if self.request.user.is_authenticated():
#             user = self.request.user
#
#         VisitLog.objects.create(content_type=self.content_type, ip_address=get_client_ip(self.request),
#                                 object_pk=self.obj.id, in_app=True, user=user)
#
#         self.obj.app_visitor_count += 1
#
#         self.obj.visitor_count = self.obj.app_visitor_count + self.obj.site_visitor_count
#
#         self.obj.save()
#
#
# class VisitLog(models.Model):
#     created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
#     content_type = models.ForeignKey(ContentType,
#                                      verbose_name='content type',
#                                      related_name="content_type_set_for_%(class)s")
#     object_pk = models.IntegerField('Object ID')
#     ip_address = GenericIPAddressField()
#
#     in_app = models.BooleanField(default=False, verbose_name="در نرم افزار")
#
#     user = models.ForeignKey('account.Profile', verbose_name="کاربر", null=True, blank=True)
#
#     class Meta:
#         verbose_name = "لاگ بازدید"
#         verbose_name_plural = "لاگ های بازدید"
#
#
# class UserAppLog(models.Model):
#     created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
#     device_id = models.CharField(verbose_name="کد دستگاه", max_length=255, default="", null=True, blank=True)
#     sdk_int = models.IntegerField(verbose_name="کد ورژن اندروید", null=True, blank=True)
#     sdk_name = models.CharField(verbose_name="ورژن اندروید", max_length=255, default="", null=True, blank=True)
#
#     app_version_code = models.IntegerField(verbose_name="کد ورژن نرم افزار", null=True, blank=True)
#     app_version_name = models.CharField(verbose_name="ورژن نرم افزار", max_length=255, default="", null=True,
#                                         blank=True)
#
#     device_name = models.CharField(verbose_name="مدل گوشی", max_length=255, default="", null=True, blank=True)
#
#     first_enter = models.BooleanField(default=False, verbose_name="اولین ورود")
#
#     ip_address = GenericIPAddressField()
#
#     user = models.ForeignKey('account.Profile', verbose_name="کاربر", null=True, blank=True)
#
#     class Meta:
#         verbose_name = "لاگ بازدید"
#         verbose_name_plural = "لاگ های بازدید"
#
#
# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
