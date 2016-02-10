from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
from django_select2.fields import AutoModelSelect2TagField, AutoModelSelect2Field
from django_select2.widgets import AutoHeavySelect2Widget, AutoHeavySelect2TagWidget
from utils.persian import arToPersianChar

__author__ = 'M.Y'


# class TitledMultipleModelField(AutoModelSelect2TagField):
#     search_fields = ['title__icontains']
#     queryset = None  # IS REQUIRED
#
#     def get_model_field_values(self, value):
#         return {'title': value}


class TitledModelWidget(AutoHeavySelect2Widget):
    def init_options(self):
        self.options['createSearchChoice'] = '*START*createIfNotExist*END*'

        # def render_texts_for_value(self, id_, value, choices):
        #     empty_values = getattr(self.field, 'empty_values', validators.EMPTY_VALUES)
        #     if value is not None and (self.field is None or value not in empty_values):
        #         try:
        #             value = int(value)
        #             values = [value]
        #             texts = self.render_texts(values, choices)
        #             if texts:
        #                 return "$('#%s').txt(%s);" % (id_, texts)
        #         except:
        #             pass


class TitledModelField(AutoModelSelect2Field):
    search_fields = ['name__icontains']
    widget = TitledModelWidget
    empty_values = list(validators.EMPTY_VALUES)
    default_error_messages = {
        'invalid_choice': "مقدار انتخاب شده معتبر نمی باشد",
    }

    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(TitledModelField, self).__init__(*args, **kwargs)

    def get_model_field_values(self, value):
        return {'name': value}

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or 'pk'
            value = self.queryset.get(**{key: value})
        except ValueError:
            raise ValidationError(self.error_messages['invalid_choice'])
        except self.queryset.model.DoesNotExist:
            value = self.create_new_value(value)
        return value

    def clean(self, value):
        if self.required and not value:
            raise ValidationError(self.error_messages['required'])
        elif not self.required and not value:
            return []
        key = self.to_field_name or 'pk'
        try:
            new_value = self.queryset.get(**{key: value})
        except ValueError:
            new_value = self.create_new_value(force_text(value))

        # qs = self.queryset.filter(**{'%s__in' % key: value})
        # pks = set([force_text(getattr(o, key)) for o in qs])
        # for i in range(0, len(value)):
        #     val = force_text(value[i])
        #     if val not in pks:
        #         value[i] = self.create_new_value(val)
        self.run_validators(new_value)
        return new_value

    def create_new_value(self, value):
        arg = {"title": arToPersianChar(value)}
        if self.http_request.user.is_authenticated():
            arg['creator'] = self.http_request.user
        obj = self.queryset.create(**arg)
        return obj


class TitledMultipleModelWidget(AutoHeavySelect2TagWidget):
    def init_options(self):
        super(TitledMultipleModelWidget, self).init_options()
        self.options['tokenSeparators'] = [","]
        self.options['createSearchChoice'] = '*START*django_select2.createSearchChoiceNew*END*'
        self.options['formatResult'] = '*START*django_select2.formatResult*END*'


class TitledMultipleModelField(AutoModelSelect2TagField):
    widget = TitledMultipleModelWidget
    search_fields = ['name__icontains', ]

    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(TitledMultipleModelField, self).__init__(*args, **kwargs)

    def get_model_field_values(self, value):
        creator = None
        if self.http_request:
            creator = self.http_request.user
        return {'name': arToPersianChar(value), 'creator': creator}

    def create_new_value(self, value):
        if self.queryset.filter(**self.get_model_field_values(value)).exists():
            obj = self.queryset.filter(**self.get_model_field_values(value))[0]
        else:
            obj = self.queryset.create(**self.get_model_field_values(value))
        return getattr(obj, self.to_field_name or 'pk')
