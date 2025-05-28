from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Service, ServicePayment



@receiver(post_save, sender=Service)
def create_service_payment(sender, instance, created, **kwargs):
    """
    When a Service instance is created, automatically create a corresponding
    ServicePayment instance linked via the OneToOneField.
    """
    if created:
        # Optionally, you can set a default price or leave that to be updated later.
        ServicePayment.objects.create(service=instance, price=0)
