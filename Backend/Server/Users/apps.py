from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    name = 'Users'
    verbose_name = 'کاربران'


    def ready(self):
        import Users.signals