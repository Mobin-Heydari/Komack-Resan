from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, IdCardInFormation
from Profiles.models import (
    ServiceProviderProfile,
    ServiceRecipientProfile,
    OwnerProfile,
    AdminProfile,
    SupportProfile,
)



@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    """
    When a new User instance is created:
    1. Ensure the user has an associated IdCardInFormation instance.
    2. Create the appropriate profile based on the user's type:
       - "SP" (Service Provider) → ServiceProviderProfile
       - "SC" (Service Recipient) → ServiceRecipientProfile
       - "OW" (Owner) → OwnerProfile
       - "AD" (Admin) → AdminProfile
       - "SU" (Support) → SupportProfile

    A default value ('M') is used for gender here.
    """
    if created:
        # Create an ID card instance if not provided.
        if not instance.id_card_info:
            id_card_instance = IdCardInFormation.objects.create()
            instance.id_card_info = id_card_instance
            instance.save(update_fields=["id_card_info"])

        # Map user types to their corresponding profile creation,
        # using a default gender ('M'), which you can later update.
        if instance.user_type == User.UserTypes.SERVICEPROVIDER:
            ServiceProviderProfile.objects.create(user=instance, gender='M')
        elif instance.user_type == User.UserTypes.SERVICERECIPIENT:
            ServiceRecipientProfile.objects.create(user=instance, gender='M')
        elif instance.user_type == User.UserTypes.OWNER:
            OwnerProfile.objects.create(user=instance, gender='M')
        elif instance.user_type == User.UserTypes.ADMIN:
            AdminProfile.objects.create(user=instance, gender='M')
        elif instance.user_type == User.UserTypes.SUPPORT:
            SupportProfile.objects.create(user=instance, gender='M')
