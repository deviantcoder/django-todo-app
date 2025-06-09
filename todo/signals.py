from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Category


User = get_user_model()


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        default_categories = getattr(settings, 'DEFAULT_CATEGORIES', [])
        categories = [
            Category(user=instance, name=name) for name in default_categories
        ]
        Category.objects.bulk_create(categories)
