from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Op(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ops', on_delete=models.CASCADE)

    script = models.TextField()
    callback_url = models.CharField(max_length=2048, blank=True, default='')
    status = models.CharField(max_length=512, blank=True, default='PENDING')

    # Updated when requested? May be removed in favor of a serializer method
    info = models.TextField(blank=True, default='')


# Add a token upon user creation
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
