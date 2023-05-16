from django.db import models
from django.conf import settings

class Movie(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length = 255)
    year = models.PositiveIntegerField()

    class Meta:
        # This model is created by .sql script and is not managed by Django
        managed = False
