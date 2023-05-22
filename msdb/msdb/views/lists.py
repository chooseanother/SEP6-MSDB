from django.http import JsonResponse

from msdb.models import List
from msdb.models import Movie
from msdb.users.models import User


def toggle_list(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        movie_id = request.POST.get("movie_id")
        list_type = request.POST.get("list_type")

        user = User.objects.get(id=user_id)
        movie_list = user.lists.get(list_type=list_type)
        movie = Movie.objects.get(id=movie_id)
        is_in_list = movie in movie_list.movies.all()

        if is_in_list:
            # remove from list
            movie_list.movies.remove(movie)
            return JsonResponse({"action": "remove", "message": "Testing"}, status=200)
        else:
            # add to list
            movie_list.movies.add(movie)
            return JsonResponse({"action": "add", "message": "Testing"}, status=200)

        # todo: when adding to watchlist/watched, remove it from the other one if it is there (exclusive lists)

    return JsonResponse({}, status=400)

