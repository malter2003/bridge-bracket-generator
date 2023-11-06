from django.db import models
from django.urls import reverse

class Tournament(models.Model):
    creator = models.CharField("Creator", max_length=200)
    title = models.CharField("Title", max_length=200)
    players = models.TextField(null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("tournament-detail", args=[str(self.id)])