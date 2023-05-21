from django.shortcuts import render

from msdb.models import Movie

def person(request, person_name):
    movies_director = Movie.objects.filter(director__icontains=person_name)
    movies_actor = Movie.objects.filter(actors__icontains=person_name)

    if not movies_director and not movies_actor:
        return render(request, "404.html", dict(person_name=person_name))

    context = dict(person=person_name, movies_director=movies_director, movies_actor=movies_actor)
    return render(request, "person/person.html", context)
