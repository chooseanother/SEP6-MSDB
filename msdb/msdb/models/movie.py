from django.db import models
class Movie(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length = 255)
    year = models.PositiveIntegerField()
