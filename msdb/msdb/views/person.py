from django.shortcuts import render
from django.db.models import Avg
import datetime

from msdb.models import Movie

def person(request, person_name):
    movies_director = Movie.objects.filter(director__icontains=person_name).annotate(avg_rating=Avg('reviews__rating')).order_by('avg_rating')
    movies_actor = Movie.objects.filter(actors__icontains=person_name).annotate(avg_rating=Avg('reviews__rating')).order_by('avg_rating')

    movies_director1 = movies_director[:6]
    movies_actor1 = movies_actor[:6]
    movies_director2 = movies_director[6:]
    movies_actor2 = movies_actor[6:]

    if movies_director:
        first_year_director = Movie.objects.filter(director__icontains=person_name).order_by('year').first()
        last_year_director = Movie.objects.filter(director__icontains=person_name).order_by('-year').first()

    if movies_actor:
        first_year_actor = Movie.objects.filter(actors__icontains=person_name).order_by('year').first()
        last_year_actor = Movie.objects.filter(actors__icontains=person_name).order_by('-year').first()

    if movies_director and movies_actor:
        first_year = min(first_year_director.year, first_year_actor.year)
        last_year = max(last_year_director.year, last_year_actor.year)
    else:
        if movies_director:
            first_year = first_year_director.year
            last_year = last_year_director.year
        if movies_actor:
            first_year = first_year_actor.year
            last_year = last_year_actor.year

    current_year = datetime.date.today().year
    if last_year+1 >= current_year:
        last_year = "now"

    if not movies_director and not movies_actor:
        return render(request, "404.html", dict(person_name=person_name))

    context = dict(person=person_name, movies_director1=movies_director1, movies_director2=movies_director2,
                   movies_actor1=movies_actor1, movies_actor2=movies_actor2, first_year=first_year, last_year=last_year)
    return render(request, "person/person.html", context)
