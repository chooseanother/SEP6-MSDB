from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from msdb.views.home import home
from msdb.views.movie import movie
from msdb.views.search import search
from msdb.views.person import person
from msdb.views.movie import add_review, edit_review
from msdb.views.lists import toggle_list
from msdb.views.review import review

urlpatterns = [
    path("", home, name="home"),
    path("search/", search, name="search"),
    path("movie/<str:movie_id>", movie, name="movie"),
    path("toggle/", toggle_list, name="toggle_list"),
    path("person/<str:person_name>", person, name="person"),
    path("review/<str:review_id>", review, name="review"),
    path("add_review/<str:movie_id>", add_review, name="add_review"),
    path("edit_review/<str:movie_id>", edit_review, name="edit_review"),

    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("msdb.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
