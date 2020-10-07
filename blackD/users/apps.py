from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'blackD.users'

    
    def ready(self):
        import users.signals