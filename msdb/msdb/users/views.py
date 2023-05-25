from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.shortcuts import render

from msdb.models import List

User = get_user_model()

def user_detail_view(request, pk):

    user = User.objects.get(id=pk)

    reviews1 = user.reviews.all().order_by('-created_at')[:4]
    reviews2 = user.reviews.all().order_by('-created_at')[4:]

    if List.objects.filter(user_id=user.id):
        favorites = user.lists.get(list_type=List.ListChoices.FAVORITES)
        favorites1 = favorites.movies.all()[:6]
        favorites2 = favorites.movies.all()[6:]

        watchlist = user.lists.get(list_type=List.ListChoices.WATCHLIST)
        watchlist1 = watchlist.movies.all()[:6]
        watchlist2 = watchlist.movies.all()[6:]

        watched = user.lists.get(list_type=List.ListChoices.WATCHED)
        watched1 = watched.movies.all()[:6]
        watched2 = watched.movies.all()[6:]

    else:
        favorites1 = None
        favorites2 = None
        watchlist1 = None
        watchlist2 = None
        watched1 = None
        watched2 = None


    context = dict(me=request.user, user=user,
                   reviews1=reviews1, reviews2=reviews2,
                   favorites1=favorites1, favorites2=favorites2,
                   watchlist1=watchlist1, watchlist2=watchlist2,
                   watched1=watched1, watched2=watched2)

    return render(request, "users/user_detail.html", context)


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert self.request.user.is_authenticated  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()
