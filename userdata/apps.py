from django.apps import AppConfig

class UserdataConfig(AppConfig):
    name = 'userdata'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import userdata.signals
