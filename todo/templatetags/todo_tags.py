from django import template
from django.utils.timezone import make_aware
from datetime import datetime

register = template.Library()


@register.filter
def make_aware_datetime(value):
    if isinstance(value, datetime):
        return value
    return make_aware(datetime.combine(value, datetime.min.time()))
