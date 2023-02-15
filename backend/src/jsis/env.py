import os

SERVER_DOMAIN = os.environ.get('SERVER_DOMAIN', '')
FRONTEND_DOMAIN = os.environ.get('FRONTEND_DOMAIN', '')

DJANGO_SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')

NEIS_API_KEY = os.environ.get('NEIS_API_KEY', '')

SENTRY_DSN = os.environ.get('SENTRY_DSN', '')

DATABASE_USER = os.environ.get('DATABASE_USER', '')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', '')

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
