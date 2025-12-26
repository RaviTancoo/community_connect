from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application
from notifications.models import Notification


@receiver(post_save, sender=Application)
def create_application_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.opportunity.organization,
            message=f"{instance.volunteer.username} applied to {instance.opportunity.title}"
        )
