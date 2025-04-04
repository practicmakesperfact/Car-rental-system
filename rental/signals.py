from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking,Reward

@receiver(post_save, sender=Booking)
def add_loyality_points(sender,instance,**Kwargs):
        """ add loyalty points when a booking is marked as completed. """
        if instance.status == 'Completed':
            reward,created = Reward.objects.get_or_create(user=instance.user)
            points_earned = int(instance.total_price//100)
            reward.add_points(points_earned)

