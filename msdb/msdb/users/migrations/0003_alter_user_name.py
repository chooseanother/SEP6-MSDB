# Generated by Django 4.1.9 on 2023-05-15 14:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=255, unique=True, verbose_name="Name of User"),
        ),
    ]
