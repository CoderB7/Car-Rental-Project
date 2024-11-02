from django.apps import AppConfig


class RentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.rent'

    def ready(self):
        import apps.rent.tasks
        