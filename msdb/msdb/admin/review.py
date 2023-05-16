from django.contrib import admin

from msdb.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "movie",
        "user",
        "rating",
        "created_at",
        "updated_at",
    ]