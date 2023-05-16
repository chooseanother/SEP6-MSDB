import pytest

from msdb.users.models import User
from msdb.users.tests.factories import UserFactory


@pytest.hookimpl(tryfirst=True)
def pytest_runtestloop():
    from django.apps import apps
    unmanaged_models = []
    for app in apps.get_app_configs():
        unmanaged_models += [m for m in app.get_models()
                             if not m._meta.managed]
    for m in unmanaged_models:
        m._meta.managed = True

@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()
