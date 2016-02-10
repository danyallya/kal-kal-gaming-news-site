# -*- coding: utf-8 -*-
import datetime
from utils.calverter import gregorian_to_jalali, gregorian_to_jalali_month_year, MONTH_NAMES
from calendar import monthrange

from django import template

register = template.Library()


@register.filter
def pdate_if_date(value):
    if isinstance(value, datetime.date):
        return gregorian_to_jalali(value)
    if value is None or value == 'None' or value == '':
        return '---'
    return value


def monthdelta(d1, d2):
    delta = 0
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += datetime.timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    return delta


def month_bet(d1, d2):
    first_year, first_month = gregorian_to_jalali_month_year(d1)
    finish_year, finish_month = gregorian_to_jalali_month_year(d2)

    res = []

    while True:
        code_name = "%s-%s" % (first_year, first_month)
        ver_name = "%s %s" % (MONTH_NAMES[first_month - 1], first_year)
        res.append(
            (code_name, ver_name),
        )

        first_month += 1
        if first_month > 12:
            first_year += 1
            first_month = 1

        if first_year >= finish_year and first_month > finish_month:
            break

    return reversed(res)
