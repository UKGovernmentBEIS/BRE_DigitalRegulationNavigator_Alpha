from django.apps import AppConfig


class TrackerConfig(AppConfig):
    name = "drnalpha.tracker"

    def ready(self):
        from . import signals  # noqa: F401
