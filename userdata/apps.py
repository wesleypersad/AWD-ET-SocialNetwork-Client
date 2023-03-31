from django.apps import AppConfig

class UserdataConfig(AppConfig):
    name = 'userdata'

    def ready(self):
        import userdata.signals
