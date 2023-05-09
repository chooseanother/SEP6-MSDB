from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "msdb.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import msdb.users.signals  # noqa: F401
        except ImportError:
            pass
