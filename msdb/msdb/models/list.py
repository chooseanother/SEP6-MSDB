from django.db import models
from django.utils.translation import gettext_lazy as _

from .movie import Movie


class List(models.Model):
    class ListChoices(models.TextChoices):
        FAVORITES = "FA", _("Favorites")
        WATCHLIST = "LI", _("Watchlist")
        WATCHED = "WA", _("Watched")

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="lists", null=False, blank=False)
    list_type = models.CharField(
        max_length=2,
        choices=ListChoices.choices,
        default=ListChoices.FAVORITES,
    )
    movies = models.ManyToManyField(Movie)

