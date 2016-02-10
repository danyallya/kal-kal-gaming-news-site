# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe
from utils.calverter import jalali_to_gregorian, gregorian_to_jalali
from django.templatetags.static import static

__author__ = 'M.Y'
from django import forms


class ShamsiWidget(forms.DateInput):
    year_range = '-50:+50'

    class Media:
        js = SELECT2_WIDGET_JS = [
            static('datepicker/scripts/jquery.ui.datepicker-cc.all.min.js'),
            static('datepicker/scripts/jquery.ui.core.js'),
            # static('datepicker/scripts/jquery.ui.datepicker-cc.js'),
            static('datepicker/scripts/calendar.js'),
            static('datepicker/scripts/jquery.ui.datepicker-cc-fa.js'),
            # static('datepicker/scripts/jquery.ui.datepicker-cc-fa.js'),
            # static('datepicker/scripts/jquery.ui.datepicker-cc-fa.js'),
        ]
        css = {
            # 'screen': [
            #     static(SELECT2_CSS)
            # ],
        }

    def render(self, name, value, attrs=None):
        value = gregorian_to_jalali(value)
        html = super(ShamsiWidget, self).render(name, value, attrs)
        js = """
        <script type='text/javascript'>
            $('#id_%s').addClass('datepicker');
            $('#id_%s').datepicker({
                changeMonth: true,
                changeYear: true,
                yearRange:'%s',
                dateFormat: 'yy/mm/dd'
            });
        </script>
        """ % (name, name, self.year_range)
        return mark_safe(u"%s %s" % (html, js))

    def value_from_datadict(self, data, files, name):
        shamsi_val = data.get(name, None)
        miladi_val = jalali_to_gregorian(shamsi_val)
        if miladi_val:
            return miladi_val.isoformat()
        else:
            return miladi_val


class PersonShamsiWidget(ShamsiWidget):
    year_range = '1290:1400'


class ShamsiDateField(forms.DateField):
    widget = ShamsiWidget

    def to_python(self, value):
        return super(ShamsiDateField, self).to_python(value)
