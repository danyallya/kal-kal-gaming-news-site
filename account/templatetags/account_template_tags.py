# -*- coding:utf-8 -*-


__author__ = 'M.Y'
from django import template

register = template.Library()


@register.filter
def get_id(val):
    return val.id if val else None
