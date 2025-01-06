from django.apps import AppConfig

class DgaAppConfig(AppConfig):
    name = 'DgaApp'

    def ready(self):
        from . import views
        views.start_mqtt()
