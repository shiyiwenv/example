from django.dispatch import Signal
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_save, post_save
from models import Status


@receiver(pre_save, sender=Status)
def single_handler(sender, **kwargs):
    print('pre_save')
