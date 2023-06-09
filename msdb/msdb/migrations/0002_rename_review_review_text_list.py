# Generated by Django 4.2.1 on 2023-05-22 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("msdb", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="review",
            old_name="review",
            new_name="text",
        ),
        migrations.CreateModel(
            name="List",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "list_type",
                    models.CharField(
                        choices=[("FA", "Favorites"), ("LI", "Watchlist"), ("WA", "Watched")],
                        default="FA",
                        max_length=2,
                    ),
                ),
                ("movies", models.ManyToManyField(to="msdb.movie")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="lists", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]
