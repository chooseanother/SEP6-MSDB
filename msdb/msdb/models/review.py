from django.db import models

from .movie import Movie


class Review(models.Model):
    # Rating choices from 1 to 5
    RATING_CHOICES = [(i, f"{i}") for i in range(1, 6)]

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews", null=False, blank=False)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews", null=False, blank=False)
    rating = models.IntegerField(choices=RATING_CHOICES, null=False, blank=False)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
