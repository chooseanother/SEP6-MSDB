from django.shortcuts import render
import datetime
import random

from msdb.models import Movie

def home(request):
    current_year =datetime.date.today().year
    hot_stuff = Movie.objects.filter(year=current_year).filter(poster_url__isnull=False)[:5]
    top_10 = Movie.objects.filter(director__icontains='Tim Burton')[:10]

    context = dict(hot_stuff=hot_stuff, top_10=top_10, current_year=current_year)
    return render(request, "movies/movies_home.html", context)
