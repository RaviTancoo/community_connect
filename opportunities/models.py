from django.db import models
from django.conf import settings
from .utils import geocode_location  # <-- import from the same folder

User = settings.AUTH_USER_MODEL

class Opportunity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    organization = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='opportunities'
    )
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    required_skills = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # Automatically geocode on save
    def save(self, *args, **kwargs):
        if self.location and (self.latitude is None or self.longitude is None):
            self.latitude, self.longitude = geocode_location(self.location)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Opportunity"
        verbose_name_plural = "Opportunities"
