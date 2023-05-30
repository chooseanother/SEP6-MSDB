import datetime

from django.db.models import Avg, F
from django.shortcuts import render

from msdb.models import Movie


def home(request):
    current_year = datetime.date.today().year
    hot_stuff = Movie.objects.filter(year=current_year).filter(poster_url__isnull=False)[:5]
    top_10 = Movie.objects.annotate(avg_rating=Avg("reviews__rating")).order_by(F("avg_rating").desc(nulls_last=True))[
        :10
    ]

    context = dict(hot_stuff=hot_stuff, top_10=top_10, current_year=current_year)
    return render(request, "movies/movies_home.html", context)
