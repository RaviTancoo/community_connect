from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from opportunities.models import Opportunity
from notifications.models import Notification  # Make sure notifications app exists

User = settings.AUTH_USER_MODEL

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    volunteer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    hours_logged = models.PositiveIntegerField(null=True, blank=True)
    hours = models.PositiveIntegerField(default=0)
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ('volunteer', 'opportunity')

    def __str__(self):
        return f"{self.volunteer} → {self.opportunity}"


# ---------------- SIGNAL ----------------
@receiver(post_save, sender=Application)
def create_application_notification(sender, instance, created, **kwargs):
    """
    Automatically create a notification for the organization when
    a volunteer applies to an opportunity.
    """
    if created:
        Notification.objects.create(
            user=instance.opportunity.organization,
            message=f"{instance.volunteer.username} has applied to your opportunity '{instance.opportunity.title}'"
        )
