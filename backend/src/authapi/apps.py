'''
Application configuration for the authapi.
'''

from django.apps import AppConfig


class AuthapiConfig(AppConfig):
    """
    Application configuration class for the authapi.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapi'
