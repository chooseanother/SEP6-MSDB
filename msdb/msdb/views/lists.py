from django.http import JsonResponse

from msdb.models import List, Movie
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
            return_message = "Movie removed from "
            match list_type:
                case "WA":
                    return_message += "watched."
                case "LI":
                    return_message += "watchlist."
                case "FA":
                    return_message += "favorites."
            return JsonResponse({"action": "remove", "message": return_message}, status=200)
        else:
            # add to list
            movie_list.movies.add(movie)
            return_message = "Movie added to "
            match list_type:
                case "WA":
                    return_message += "watched."
                    # if added to watched, remove from watchlist
                    li = user.lists.get(list_type=List.ListChoices.WATCHLIST)
                    if movie in li.movies.all():
                        li.movies.remove(movie)
                        return_message += "\nMovie removed from watchlist. "
                case "LI":
                    return_message += "watchlist."
                    # if added to watchlist, remove from watched
                    if list_type == "LI":
                        wa = user.lists.get(list_type=List.ListChoices.WATCHED)
                        if movie in wa.movies.all():
                            wa.movies.remove(movie)
                            return_message += "\nMovie removed from watched. "
                case "FA":
                    return_message += "favorites."

            return JsonResponse({"action": "add", "message": return_message}, status=200)

    return JsonResponse({}, status=400)
