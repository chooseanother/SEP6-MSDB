from django.contrib import admin

from msdb.models import List

@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "list_type"
    ]
