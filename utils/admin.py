# -*- coding:utf-8 -*-
from django import forms
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django_select2.fields import AutoModelSelect2Field, AutoModelSelect2MultipleField
from multiselectfield.db.fields import MultiSelectField
from solo.admin import SingletonModelAdmin
from easy_select2.utils import select2_modelform
# from mce_filebrowser.admin import MCEFilebrowserAdmin
from easy_select2.widgets import Select2Multiple
from movie.models import BaseMovie, WEEK_DAY
from person.models import Person, MovieCompany
from utils.calverter import jalali_by_time
from utils.date import handel_date_fields
from utils.fields.date_fields import ShamsiWidget
from utils.fields.select2 import TitledModelField, TitledMultipleModelField
from utils.forms import BaseForm
from utils.models import SiteConfig, UserAppLog

__author__ = 'M.Y'


class PersonChoiceField(TitledModelField):
    queryset = Person.objects


class PersonMultipleChoiceField(TitledMultipleModelField):
    queryset = Person.objects


class CompanyMultipleChoiceField(TitledMultipleModelField):
    queryset = MovieCompany.objects


class AdminModelForm(BaseForm):
    shamsi_widget = ShamsiWidget

    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(AdminModelForm, self).__init__(*args, **kwargs)

        self.process_form()

    def process_form(self):
        for name, field in self.fields.items():
            if isinstance(field, forms.ModelMultipleChoiceField):
                field.help_text = ""

        for field in self._meta.model._meta.many_to_many:
            if field.related_model is Person and field.name in self.fields:
                old_field = self.fields[field.name]
                self.fields[field.name] = PersonMultipleChoiceField(required=old_field.required,
                                                                    label=old_field.label,
                                                                    http_request=self.http_request)
            if field.related_model is MovieCompany and field.name in self.fields:
                old_field = self.fields[field.name]
                self.fields[field.name] = CompanyMultipleChoiceField(required=old_field.required,
                                                                     label=old_field.label,
                                                                     http_request=self.http_request)

        for field in self._meta.model._meta.fields:
            if field.related_model is BaseMovie and field.name in self.fields:
                old_field = self.fields[field.name]
                self.fields[field.name] = RelatedMovieChoiceField(required=old_field.required,
                                                                  label=old_field.label)

                # elif field.related_model is Person and field.name in self.fields:
                #     old_field = self.fields[field.name]
                #     self.fields[field.name] = RelatedPersonChoiceField(required=old_field.required,
                #                                                        label=old_field.label)

        handel_date_fields(self, self.shamsi_widget)


class HardModelAdmin(admin.ModelAdmin):
    save_as = True

    form_class = AdminModelForm

    def __init__(self, model, admin_site):
        self.num = 0
        self.form = select2_modelform(model, attrs={'width': '250px'}, form_class=self.form_class)
        super(HardModelAdmin, self).__init__(model, admin_site)
        # self.list_display = ['get_row_num'] + list(self.list_display)
        if 'created_on' in model._meta.get_all_field_names() and 'get_created_date' not in self.list_display:
            self.list_display = list(self.list_display) + ['get_created_date']
        if 'creator' in model._meta.get_all_field_names():
            self.exclude = [] if not self.exclude else self.exclude
            if 'creator' not in self.exclude:
                self.exclude += ['creator', ]
        if not self.list_display_links:
            self.list_display_links = self.list_display[:2]
            # self.list_editable = ['name']

    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super(HardModelAdmin, self).get_form(request, obj, **kwargs)

        class AdminFormWithRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['http_request'] = request
                return AdminForm(*args, **kwargs)

        return AdminFormWithRequest

    def get_created_date(self, obj):
        return jalali_by_time(obj.created_on)

    get_created_date.short_description = u"تاریخ ایجاد"
    get_created_date.admin_order_field = 'created_on'

    def get_row_num(self, obj):
        self.num += 1
        return self.num

    get_row_num.short_description = u"ردیف"

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        obj.save()


class RelatedPersonMultipleChoiceField(AutoModelSelect2MultipleField):
    queryset = Person.objects
    search_fields = ['name__icontains']


class RelatedMovieChoiceField(AutoModelSelect2Field):
    queryset = BaseMovie.objects
    search_fields = ['name__icontains']


class RelatedPersonChoiceField(AutoModelSelect2Field):
    queryset = Person.objects
    search_fields = ['name__icontains']


class AdminInlineModelForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(AdminInlineModelForm, self).__init__(*args, **kwargs)
        self.process_form()

    def process_form(self):
        for name, field in self.fields.items():
            if isinstance(field, forms.ModelMultipleChoiceField):
                field.help_text = ""

        for field in self._meta.model._meta.many_to_many:
            if field.related_model is Person and field.name in self.fields:
                old_field = self.fields[field.name]
                self.fields[field.name] = RelatedPersonMultipleChoiceField(required=old_field.required,
                                                                           label=old_field.label)

        for field in self._meta.model._meta.fields:
            if isinstance(field, ForeignKey) and field.related_model is BaseMovie and field.name in self.fields:
                old_field = self.fields[field.name]
                self.fields[field.name] = RelatedMovieChoiceField(required=old_field.required,
                                                                  label=old_field.label)

            if isinstance(field, MultiSelectField):
                self.fields[field.name].widget = Select2Multiple(choices=WEEK_DAY)


class HardTabularInline(admin.TabularInline):
    form = AdminInlineModelForm

    def __init__(self, model, admin_site):
        super(HardTabularInline, self).__init__(model, admin_site)


class SiteConfigAdmin(SingletonModelAdmin):
    def save_related(self, request, form, formsets, change):
        super(SiteConfigAdmin, self).save_related(request, form, formsets, change)
        form.instance.update()


admin.site.register(SiteConfig, SiteConfigAdmin)


class UserAppLogAdmin(HardModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    readonly_fields = UserAppLog._meta.get_all_field_names()


admin.site.register(UserAppLog, UserAppLogAdmin)
