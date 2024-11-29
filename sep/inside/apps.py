from django.apps import AppConfig

class InsideConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inside'

    def ready(self):
        import inside.signals


# apps.py
# from django.apps import AppConfig
#
# class YourAppConfig(AppConfig):
#     name = 'yourapp'
#
#     def ready(self):
#         import yourapp.signals
