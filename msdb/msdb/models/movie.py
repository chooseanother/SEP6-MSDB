from django.db import models
from django.contrib.postgres.fields import ArrayField

class Movie(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length = 255)
    year = models.PositiveIntegerField()
    genre = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    director = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    actors = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    poster_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # This model is created by .sql script and is not managed by Django
        managed = False
