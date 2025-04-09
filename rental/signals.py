from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking,Reward
import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Booking)
def add_loyality_points(sender,instance,**Kwargs):
        """ add loyalty points when a booking is marked as completed. """
        if instance.status == 'Completed':
            reward,created = Reward.objects.get_or_create(user=instance.user)
            points_earned = int(instance.total_price//100)
            reward.add_points(points_earned)

@receiver(post_save,sender=Booking)
def notify_user_on_completion(sender,instance,created,**kwargs):
    if not created and instance.status == 'Completed' and hasattr(instance,'payment_status') and instance.payment_status == "Paid":
        
    # ONLY SEND EMAIL IF THE STATUS CHANGED TO COMPLETED AND PAYMENT IS PAID
        subject = f"Booking {instance.id} Completed - Ethio Car Rental"
        message =f"""
        Dear {instance.user.username},
        
        We are pleased to inform you that your booking (ID:{instance.id}) has been marked as completed.
        
        Details:
        -Car:{instance.car.name}
        -Start Date:{instance.start_date}
        -End Date:{instance.end_date}
        -Total Price: ETB{instance.total_price}
        Thank you for choosing Ethio Car Rental.
        
        best regards,
        The Ethio Car Rental Team
        """
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.user.email],
                fail_silently=False,
                
            )
        except Exception as e:
            logger.error(f"faild to send email for booking {instance.id}: {str(e)}")