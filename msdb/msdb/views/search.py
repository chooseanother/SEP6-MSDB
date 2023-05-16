from django.shortcuts import render, redirect
from functools import reduce
import operator
from django.db.models import Q

from msdb.models import Movie
from msdb.users.models import User


def search(request):
    if request.method == "POST":
        search_string = request.POST.get("query")

        movies_result = Movie.objects.filter(reduce(operator.and_, (Q(title__icontains=x) for x in search_string.split(' '))))[:10]
        users_result = User.objects.filter(reduce(operator.and_, (Q(name__icontains=x) for x in search_string.split(' '))))[:10]

        context = dict(query=search_string, movies=movies_result, users=users_result)
        return render(request, "search/search.html", context)
    else:
        return redirect('home')
