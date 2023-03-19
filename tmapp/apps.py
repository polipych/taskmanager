from django.apps import AppConfig


class TmAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tmapp"

    def ready(self) -> None:
        from . import signals  # noqa

    #    import tmapp.signals
