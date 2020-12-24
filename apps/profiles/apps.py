from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'
    
    #import local signals
    def ready(self):
        import profiles.signals