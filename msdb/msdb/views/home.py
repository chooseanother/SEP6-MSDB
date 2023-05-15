from django.shortcuts import render
def home(request):
    list = {1, 2, 3, 4, 6, 8}
    context = dict(list=list)
    return render(request, "movies/movies_home.html", context)
