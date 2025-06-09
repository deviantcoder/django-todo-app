from django import template
from datetime import datetime
from django.utils.timezone import make_aware

register = template.Library()


def make_aware_datetime(value):
    if isinstance(value, datetime):
        return value
    return make_aware(datetime.combine(value, datetime.min.time()))