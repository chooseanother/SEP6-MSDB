from django.contrib.postgres.fields import ArrayField
from django.db import models


class Movie(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    genre = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    director = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    actors = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    poster_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # This model is created by .sql script and is not managed by Django
        managed = False

    @property
    def rating(self):
        return self.reviews.aggregate(models.Avg("rating"))["rating__avg"]

    @property
    def review_count(self):
        return self.reviews.count()
